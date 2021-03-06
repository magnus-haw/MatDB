from django.contrib import admin
from .models import ITARMaterial, ITARMaterialVersion, ITARVariableProperty
from .models import ITARConstProperty, ITARMatrixProperty
from materials.admin import ConstPropertyAdmin, MaterialAdmin, VariablePropertyAdmin
from materials.admin import MatrixPropertyAdmin, MaterialVersionAdmin

# Register your models here
class ITARConstPropertyAdmin(ConstPropertyAdmin):
    pass

class ITARMaterialAdmin(MaterialAdmin):
    pass

class ITARMaterialVersionAdmin(MaterialVersionAdmin):
    pass

class ITARVariablePropertyAdmin(VariablePropertyAdmin):
    pass

class ITARMatrixPropertyAdmin(MatrixPropertyAdmin):
    pass

admin.site.register(ITARMaterial,ITARMaterialAdmin)
admin.site.register(ITARMaterialVersion,ITARMaterialVersionAdmin)
admin.site.register(ITARVariableProperty,ITARVariablePropertyAdmin)
admin.site.register(ITARConstProperty, ITARConstPropertyAdmin)
admin.site.register(ITARMatrixProperty,ITARMatrixPropertyAdmin)