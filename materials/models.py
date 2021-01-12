from django.db import models
from units.models import BaseUnit, ComboUnit
import numpy as np

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

class Material(models.Model):
    name = models.CharField(max_length=500,unique=True)
    short_name = models.CharField(max_length=25,unique=True,null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

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
class MaterialVersion(models.Model):
    material = models.ForeignKey(Material,on_delete=models.CASCADE)
    version = models.CharField(max_length=25,unique=True)
    grade = models.CharField(max_length=1,choices=MATERIAL_GRADES,null=True,blank=True)
    notes = models.TextField(blank=True,null=True)
    datasheet = models.FileField(blank=True,null=True)
    date = models.DateField()
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.material.name + "_" + self.version

MATERIAL_STATES = (
    (0,'Virgin'),
    (1,'Char'),
    (2,'Pyrolysis')
)
class VariableProperties(models.Model):
    material = models.ForeignKey(MaterialVersion,on_delete=models.CASCADE)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)
    references = models.TextField(null=True,blank=True)
    last_modified = models.DateField(auto_now=True)
    
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
        verbose_name_plural = "Variable properties"

class ConstProperty(models.Model):
    material = models.ForeignKey(MaterialVersion,on_delete=models.CASCADE)
    unit = models.ForeignKey(ComboUnit,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    value = models.FloatField()
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Constant properties"

class MatrixProperty(models.Model):
    material = models.ForeignKey(MaterialVersion,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=500)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Matrix properties"

