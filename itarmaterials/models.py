from django.db import models
from materials.models import AbstractMaterial, AbstractMaterialVersion, AbstractVariableProperties
from materials.models import AbstractConstProperty, AbstractMatrixProperty, AbstractReference

#################################################################################
###########                     ITAR MATERIALS                  #################
#################################################################################

class ITARMaterial(AbstractMaterial):

    class Meta:
        verbose_name_plural = "ITAR Materials"

class ITARMaterialVersion(AbstractMaterialVersion):
    material = models.ForeignKey(ITARMaterial,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "ITAR Material versions"

class ITARVariableProperties(AbstractVariableProperties):
    material = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ITAR Variable properties"

class ITARConstProperty(AbstractConstProperty):
    material = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "ITAR Constant properties"

class ITARMatrixProperty(AbstractMatrixProperty):
    material = models.ForeignKey(ITARMaterialVersion,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "ITAR Matrix properties"

class ITARReference(AbstractReference):
    material = models.ForeignKey(ITARMaterialVersion, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = "ITAR References"