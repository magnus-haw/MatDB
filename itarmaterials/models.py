from django.db import models
from materials.models import AbstractMaterial, AbstractMaterialVersion, AbstractVariableProperty
from materials.models import AbstractConstProperty, AbstractMatrixProperty, AbstractMaterialPropertyInstance

#################################################################################
###########                     ITAR MATERIALS                  #################
#################################################################################

class ITARMaterial(AbstractMaterial):
    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Materials"

class ITARMaterialVersion(AbstractMaterialVersion):
    material = models.ForeignKey(ITARMaterial,on_delete=models.CASCADE)
    
    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Material versions"

class ITARMaterialPropertyInstance(AbstractMaterialPropertyInstance):
    material_version = models.ForeignKey(ITARMaterialVersion, on_delete=models.CASCADE)

    def isITAR(self):
        return True
    
    class Meta:
        verbose_name_plural = "ITAR Material property instances"

class ITARVariableProperty(AbstractVariableProperty):
    property_instance = models.ForeignKey(ITARMaterialPropertyInstance,on_delete=models.CASCADE, null=True,blank=False)

    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Variable properties"

class ITARConstProperty(AbstractConstProperty):
    property_instance = models.ForeignKey(ITARMaterialPropertyInstance,on_delete=models.CASCADE, null=True,blank=False)
    
    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Constant properties"

class ITARMatrixProperty(AbstractMatrixProperty):
    property_instance = models.ForeignKey(ITARMaterialPropertyInstance,on_delete=models.CASCADE, null=True,blank=False)

    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Matrix properties"

