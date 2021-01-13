from django.db import models
from django.conf import settings

from units.models import BaseUnit, ComboUnit
from contacts.models import Person

import numpy as np
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
    version = models.CharField(max_length=25,unique=True)
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
class AbstractVariableProperties(BaseModel):
    material = models.ForeignKey(MaterialVersion, on_delete=models.CASCADE)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES, default=0)
    
    # Assume using SI units for all properties
    p = MyArrayField(null=True, blank=True)
    T = MyArrayField(null=True, blank=True)
    cp = MyArrayField(null=True, blank=True)
    h = MyArrayField(null=True, blank=True)
    ki = MyArrayField(null=True, blank=True)
    kj = MyArrayField(null=True, blank=True)
    kk = MyArrayField(null=True, blank=True)
    emissivity = MyArrayField(null=True, blank=True)
    absorptivity = MyArrayField(null=True, blank=True)

    def __str__(self):
        if self.state == 0:
            mystate = "Virgin"
        elif self.state == 1:
            mystate = "Char"
        else:
            mystate = "Pyrolysis"
        return self.material.material.name + "_VariableProperties_"+ mystate

    @property
    def get_rows(self):
        arrays = [self.p,self.T,self.cp,self.h,self.ki,self.kj,self.kk,
                  self.emissivity, self.absorptivity]
        rows = []
        for i in range(0,len(self.p)):
            row=[]
            for ar in arrays:
                row.append(ar[i])
            rows.append(row)
        return rows

    class Meta:
        abstract = True

class VariableProperties(AbstractVariableProperties):

    class Meta:
        verbose_name_plural = "Variable properties"

class AbstractConstProperty(BaseModel):
    material = models.ForeignKey(MaterialVersion,on_delete=models.CASCADE)
    unit = models.ForeignKey(ComboUnit,on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    value = models.FloatField()
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)
    
    def __str__(self):
        return self.name

    class Meta:
        abstract = True

class ConstProperty(AbstractConstProperty):

    class Meta:
        verbose_name_plural = "Constant properties"

class AbstractMatrixProperty(BaseModel):
    material = models.ForeignKey(MaterialVersion,on_delete=models.CASCADE)
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
    (5,'Other')
)

class AbstractReference(BaseModel):
    material = models.ForeignKey(MaterialVersion, on_delete=models.SET_NULL, null=True)
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