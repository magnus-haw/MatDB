from django.db import models
from materials.models import AbstractMaterial, AbstractMaterialVersion, AbstractVariableProperty
from materials.models import AbstractConstProperty, AbstractMatrixProperty, AbstractMaterialProperty


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

class ITARMaterialProperty(AbstractMaterialProperty):

    def isITAR(self):
        return True
    
    class Meta:
        verbose_name_plural = "ITAR Material properties"

class ITARVariableProperty(AbstractVariableProperty):
    property = models.ForeignKey(ITARMaterialProperty,on_delete=models.CASCADE, null=True,blank=False)
    material_version = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)

    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Variable properties"

class ITARConstProperty(AbstractConstProperty):
    property = models.ForeignKey(ITARMaterialProperty,on_delete=models.CASCADE, null=True,blank=False)
    material_version = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)
    
    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Constant properties"

class ITARMatrixProperty(AbstractMatrixProperty):
    property = models.ForeignKey(ITARMaterialProperty,on_delete=models.CASCADE, null=True,blank=False)
    material_version = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)

    def isITAR(self):
        return True

    class Meta:
        verbose_name_plural = "ITAR Matrix properties"

