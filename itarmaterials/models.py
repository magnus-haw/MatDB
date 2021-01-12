from django.db import models
from materials.models import MyArrayField, MATERIAL_RATING, MATERIAL_GRADES, MATERIAL_STATES
import numpy as np

#################################################################################
###########                     ITAR MATERIALS                  #################
#################################################################################

class ITARMaterial(models.Model):
    name = models.CharField(max_length=500,unique=True)
    short_name = models.CharField(max_length=25,unique=True,null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ITAR Materials"

class ITARMaterialVersion(models.Model):
    material = models.ForeignKey(ITARMaterial,on_delete=models.CASCADE)
    version = models.CharField(max_length=50,unique=True)
    grade = models.CharField(max_length=1,choices=MATERIAL_GRADES,null=True,blank=True)
    notes = models.TextField(blank=True,null=True)
    datasheet = models.FileField(blank=True,null=True)
    date = models.DateField()
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.material.name + "_" + self.version
    
    class Meta:
        verbose_name_plural = "ITAR Material versions"

class ITARVariableProperties(models.Model):
    material = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)
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
        verbose_name_plural = "ITAR Variable properties"

class ITARConstProperty(models.Model):
    material = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    value = models.FloatField()
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ITAR Constant properties"

class ITARMatrixProperty(models.Model):
    material = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=500)
    state = models.PositiveIntegerField(choices=MATERIAL_STATES,default=0)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "ITAR Matrix properties"