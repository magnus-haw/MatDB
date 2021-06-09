from django.db import models
from django.conf import settings
from django.core.validators import int_list_validator

from units.models import BaseUnit, ComboUnit

import numpy as np
from scipy import interpolate

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

# Create your models here.

class MyArrayField(models.TextField):
    description = "A numpy array field serialized to txt"

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None:
            return None
        elif isinstance(value, np.ndarray):
            return value
        else:
            return np.fromstring(value, sep=' ')

    def get_prep_value(self, value):
        if value is None:
            return None
        else:
            strrep = np.array2string(value,threshold=np.inf,max_line_width=np.inf)
            return strrep[1:-1]

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
        null=True, blank=True, on_delete=models.SET_NULL)

    def isITAR(self):
        return False

    class Meta:
        abstract = True

class AbstractMaterial(BaseModel):
    name = models.CharField(max_length=500,unique=True)
    short_name = models.CharField(max_length=25,unique=True,null=True,blank=True)
    short_description = models.CharField(max_length=100,blank=True,null=True)
    description = RichTextField(blank=True,null=True)
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Material(AbstractMaterial):
    pass

MATERIAL_GRADES = (
    ('A','Validated'),
    ('B','Limited Validation'),
    ('C','Low Confidence Tests'),
    ('D','Estimate Only'),
    ('F','Inconsistent')
)

def get_version_value(version, delimiter='.'):
    """Serialize a version string into a sortable integer. valid up to subfields of 99 

    Args:
        version (str): string consisting of integers separated by periods: 'X.X.X' 
        delimiter (str, optional): Defaults to '.'

    Returns:
        ret (int): integer equivalent of version string
    """
    vlist = version.split(delimiter)
    ret = 0.
    for i,v in enumerate(vlist):
        ret += (10**(8-2*i) )*int(v)
    return int(ret)

class AbstractMaterialVersion(BaseModel):
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    version = models.CharField(max_length=25, validators=[int_list_validator(sep='.')])
    version_value = models.PositiveIntegerField(null=True,blank=True)
    grade = models.CharField(max_length=1,choices=MATERIAL_GRADES,null=True,blank=True)
    material_lead = models.ForeignKey('sources.Person', blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_material_lead')
    material_expert = models.ForeignKey('sources.Person', blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_material_expert')
    modeling_expert = models.ForeignKey('sources.Person', blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_modeling_expert')
    other_contact = models.ForeignKey('sources.Person', blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_other_contact')
    notes = models.TextField(blank=True,null=True)
    datasheet = models.FileField(blank=True,null=True)
    published = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.material.name + "_" + self.version

    def save(self, *args, **kwargs):
        self.version_value = get_version_value(self.version) # enforce version serialization
        super().save(*args, **kwargs)  # Call the parent save() method.

    class Meta:
        abstract = True
        unique_together = ('material', 'version',)
        ordering = ['-version_value']

class MaterialVersion(AbstractMaterialVersion):
    pass

MATERIAL_STATES = (
    (0,'Virgin'),
    (1,'Char'),
    (2,'Pyrolysis')
)

class AbstractMaterialProperty(BaseModel):
    name = models.CharField(max_length=50)
    description = RichTextField(blank=True,null=True)
    unit = models.ForeignKey(ComboUnit,on_delete=models.SET_NULL, null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class MaterialProperty(AbstractMaterialProperty):
    
    class Meta:
        verbose_name_plural = "Material properties"

class AbstractMaterialPropertyInstance(BaseModel):
    property = models.ForeignKey(MaterialProperty,on_delete=models.CASCADE, null=True,blank=False)
    material_version = models.ForeignKey(MaterialVersion, on_delete=models.CASCADE)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES, default=0, verbose_name='Material state')

    def __str__(self):
        return str(self.material_version) + "_" + str(self.state) + "_" + self.property.name

    class Meta:
        abstract = True

class MaterialPropertyInstance(AbstractMaterialPropertyInstance):
    
    class Meta:
        verbose_name_plural = "Material property instances"

class AbstractVariableProperty(BaseModel):
    property_instance = models.ForeignKey(MaterialPropertyInstance,on_delete=models.CASCADE, null=True,blank=False)
    
    # using SI units for p,T
    p = MyArrayField(null=True, blank=True, verbose_name='Pressure [Pa]') #Pascals
    T = MyArrayField(null=True, blank=True, verbose_name='Temperature [K]') #Kelvin
    values = MyArrayField(null=True, blank=True)
    
    def __str__(self):
        return "varprop_" + str(self.property_instance)

    def interp(self,new_p,new_T):
        f = interpolate.interp2d(self.p,self.T,self.values, kind='linear')
        return f(new_p,new_T)

    class Meta:
        abstract = True

class VariableProperty(AbstractVariableProperty):

    class Meta:
        verbose_name_plural = "Variable properties"

class AbstractConstProperty(BaseModel):
    property_instance = models.ForeignKey(MaterialPropertyInstance,on_delete=models.CASCADE, null=True,blank=False)
    value = models.FloatField(null=True)

    def __str__(self):
        return "constprop_" + str(self.property_instance)

    class Meta:
        abstract = True

class ConstProperty(AbstractConstProperty):

    class Meta:
        verbose_name_plural = "Constant properties"

class AbstractMatrixProperty(BaseModel):
    property_instance = models.ForeignKey(MaterialPropertyInstance,on_delete=models.CASCADE, null=True,blank=False)
    value = models.CharField(max_length=500)

    def __str__(self):
        return "matrixprop_" + str(self.property_instance)

    class Meta:
        abstract = True

class MatrixProperty(AbstractMatrixProperty):

    class Meta:
        verbose_name_plural = "Matrix properties"
