from django.db import models
from django.conf import settings

from units.models import BaseUnit, ComboUnit
from contacts.models import Person

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
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class Material(AbstractMaterial):
    pass


MATERIAL_RATING = (
    (0,'Untested'),
    (1,'Tested'),
    (2,'Validated')
)

MATERIAL_GRADES = (
    ('A','Validated'),
    ('B','Limited Validation'),
    ('C','Low Confidence Tests'),
    ('D','Estimate Only'),
    ('F','Inconsistent')
)
class AbstractMaterialVersion(BaseModel):
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    version = models.CharField(max_length=25)
    grade = models.CharField(max_length=1,choices=MATERIAL_GRADES,null=True,blank=True)
    material_lead = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_material_lead')
    material_expert = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_material_expert')
    modeling_expert = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_modeling_expert')
    other_contact = models.ForeignKey(Person, blank=True, null=True, on_delete=models.CASCADE, related_name='%(class)s_other_contact')
    notes = models.TextField(blank=True,null=True)
    datasheet = models.FileField(blank=True,null=True)
    published = models.DateField(blank=True,null=True)

    def __str__(self):
        return self.material.name + "_" + self.version

    class Meta:
        abstract = True

class MaterialVersion(AbstractMaterialVersion):
    pass

MATERIAL_STATES = (
    (0,'Virgin'),
    (1,'Char'),
    (2,'Pyrolysis')
)

class AbstractVariableProperty(BaseModel):
    material_version = models.ForeignKey(MaterialVersion, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    unit = models.ForeignKey(ComboUnit,on_delete=models.SET_NULL, null=True,blank=True)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES, default=0, verbose_name='Material state')
    # using SI units for p,T
    p = MyArrayField(null=True, blank=True, verbose_name='Pressure [Pa]') #Pascals
    T = MyArrayField(null=True, blank=True, verbose_name='Temperature [K]') #Kelvin
    values = MyArrayField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    def interp(self,new_p,new_T):
        f = interpolate.interp2d(self.p,self.T,self.values, kind='linear')
        return f(new_p,new_T)

    class Meta:
        abstract = True

class VariableProperty(AbstractVariableProperty):

    class Meta:
        verbose_name_plural = "Variable properties"

class AbstractConstProperty(BaseModel):
    material_version = models.ForeignKey(MaterialVersion,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    unit = models.ForeignKey(ComboUnit,on_delete=models.SET_NULL, null=True,blank=True)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)
    description = models.TextField(null=True,blank=True)
    value = models.FloatField(null=True)
        
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class ConstProperty(AbstractConstProperty):

    class Meta:
        verbose_name_plural = "Constant properties"

class AbstractMatrixProperty(BaseModel):
    material_version = models.ForeignKey(MaterialVersion,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=500)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class MatrixProperty(AbstractMatrixProperty):

    class Meta:
        verbose_name_plural = "Matrix properties"

REFERENCE_TYPES = (
    (0,'Journal article'),
    (1,'Unpublished report'),
    (2,'Book'),
    (3,'Test data'),
    (4,'Sim data'),
    (5,'Poster'),
    (6,'Presentation'),
    (7,'Other'),
)

class AbstractReference(BaseModel):
    material_version = models.ForeignKey(MaterialVersion, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length = 500)
    doc_num = models.CharField(max_length = 100, null=True, blank=True)
    reftype = models.PositiveIntegerField(choices=REFERENCE_TYPES, default=0)
    authors = models.CharField(max_length = 50)
    body = RichTextUploadingField(null=True, blank=True)
    published = models.DateField(null=True, blank=True)
    
    file = models.FileField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True

class Reference(AbstractReference):
    pass

class AbstractDownloadModel(BaseModel):
    material = models.ForeignKey(MaterialVersion, on_delete=models.CASCADE)
    code_name = models.CharField(max_length=50)
    file_name = models.CharField(max_length=500)

    def __str__(self):
        return self.file_name

    class Meta:
        abstract = True

class DownloadModel(AbstractDownloadModel):

    class Meta:
        verbose_name_plural = "Download model"