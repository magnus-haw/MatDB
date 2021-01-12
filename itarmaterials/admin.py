from django.contrib import admin
from .models import ITARMaterial, ITARMaterialVersion, ITARVariableProperties, ITARConstProperty, ITARMatrixProperty

# Register your models here
class ITARConstPropertyAdmin(admin.ModelAdmin):
    list_display= ('name', 'material','state', 'value', 'description', 'last_modified')
    list_filter = ('material', 'state', 'last_modified')
    search_fields = ('name', 'material__material__name','material__version','state', 'value', 'description', 'last_modified')

class ITARMaterialAdmin(admin.ModelAdmin):
    list_display= ('name','description')
    search_fields = ('name','description')

class ITARMaterialVersionAdmin(admin.ModelAdmin):
    list_display  = ('material','version','grade','notes','date')
    list_filter = ('material', 'grade')
    search_fields = ('material__name','version','grade','notes','date')

class ITARVariablePropertiesAdmin(admin.ModelAdmin):
    list_display  = ('material','state','references','last_modified')
    search_fields = ('material__material__name','state','references','last_modified')
    list_filter = ('material', 'state', 'last_modified')

class ITARMatrixPropertyAdmin(admin.ModelAdmin):
    list_display = ('name','material','state','description','value','last_modified')
    search_fields = ('name','material__material__name','material__version','state','description','value','last_modified')
    list_filter = ('material', 'state', 'last_modified')

admin.site.register(ITARMaterial,ITARMaterialAdmin)
admin.site.register(ITARMaterialVersion,ITARMaterialVersionAdmin)
admin.site.register(ITARVariableProperties,ITARVariablePropertiesAdmin)
admin.site.register(ITARConstProperty, ITARConstPropertyAdmin)
admin.site.register(ITARMatrixProperty,ITARMatrixPropertyAdmin)