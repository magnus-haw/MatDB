from django.contrib import admin
from .models import Material, MaterialVersion, VariableProperty
from .models import ConstProperty, MatrixProperty, MaterialPropertyInstance

# Register your models here
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at','last_modified','modified_by',]

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        print(obj.modified_by)
        super().save_model(request, obj, form, change)

class ConstPropertyAdmin(BaseAdmin):
    list_display= ('property_instance','value', 'last_modified')
    list_filter = ('property_instance__material_version__material', 'last_modified')
    search_fields = ('property_instance', 'property_instance__material_version__material__name','property_instance__material_version__version','property_instance__state', 'value', 'last_modified')
    
class MaterialAdmin(BaseAdmin):
    list_display= ('name','short_description')
    search_fields = ('name','description')

class VariablePropertyAdmin(BaseAdmin):
    list_display  = ('property_instance','last_modified')
    search_fields = ('property_instance','property_instance__material_version__material__name','property_instance__state','last_modified')
    list_filter = ('property_instance__material_version__material', 'last_modified')

class MatrixPropertyAdmin(BaseAdmin):
    list_display = ('property_instance','value','last_modified')
    search_fields = ('property_instance','property_instance__material_version__material__name','property_instance__state','last_modified')
    list_filter = ('property_instance__material_version__material', 'last_modified')

class MaterialVersionAdmin(BaseAdmin):
    list_display  = ('material','version','grade','notes')
    list_filter = ('material', 'grade')
    search_fields = ('material__name','version','grade','notes')
    exclude = ('version_value',)
    #save_as = True

class MaterialPropertyInstanceAdmin(BaseAdmin):
    list_display  = ('property','material_version','state')
    list_filter = ('state', 'last_modified')
    search_fields = ('property','material_version','property__name','state')
    
admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialVersion, MaterialVersionAdmin)
admin.site.register(VariableProperty, VariablePropertyAdmin)
admin.site.register(ConstProperty, ConstPropertyAdmin)
admin.site.register(MatrixProperty, MatrixPropertyAdmin)

