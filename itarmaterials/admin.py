from django.contrib import admin
from .models import ITARMaterial, ITARMaterialVersion, ITARVariableProperty
from .models import ITARConstProperty, ITARMatrixProperty, ITARReference
from materials.admin import ConstPropertyAdmin, MaterialAdmin, VariablePropertyAdmin
from materials.admin import MatrixPropertyAdmin, MaterialVersionAdmin, ReferenceAdmin

# Register your models here
class ITARConstPropertyAdmin(ConstPropertyAdmin):
    pass

class ITARMaterialAdmin(MaterialAdmin):
    pass

class ITARReferenceAdmin(ReferenceAdmin):
    pass

class ITARReferenceInline(admin.StackedInline):
    model = ITARReference
    extra = 0
    readonly_fields = ['created_at','last_modified','modified_by',]

class ITARMaterialVersionAdmin(MaterialVersionAdmin):
    inlines = [
        ITARReferenceInline,
    ]

class ITARVariablePropertyAdmin(VariablePropertyAdmin):
    pass

class ITARMatrixPropertyAdmin(MatrixPropertyAdmin):
    pass

admin.site.register(ITARMaterial,ITARMaterialAdmin)
admin.site.register(ITARMaterialVersion,ITARMaterialVersionAdmin)
admin.site.register(ITARVariableProperty,ITARVariablePropertyAdmin)
admin.site.register(ITARConstProperty, ITARConstPropertyAdmin)
admin.site.register(ITARMatrixProperty,ITARMatrixPropertyAdmin)
admin.site.register(ITARReference,ITARReferenceAdmin)