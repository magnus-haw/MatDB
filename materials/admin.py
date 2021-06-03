from django.contrib import admin
from .models import Material, MaterialVersion, VariableProperty
from .models import ConstProperty, MatrixProperty

# Register your models here
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at','last_modified','modified_by',]

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        print(obj.modified_by)
        super().save_model(request, obj, form, change)

class ConstPropertyAdmin(BaseAdmin):
    list_display= ('property', 'material_version','value', 'last_modified')
    list_filter = ('material_version', 'last_modified')
    search_fields = ('property', 'material_version__material__name','material_version__version','property__state', 'value', 'property__description', 'last_modified')
    
class MaterialAdmin(BaseAdmin):
    list_display= ('name','short_description')
    search_fields = ('name','description')

class VariablePropertyAdmin(BaseAdmin):
    list_display  = ('property','material_version','last_modified')
    search_fields = ('property','material_version__material__name','property__state','last_modified')
    list_filter = ('material_version', 'last_modified')

class MatrixPropertyAdmin(BaseAdmin):
    list_display = ('property','material_version','value','last_modified')
    search_fields = ('property','material_version__material__name','material_version__version','property__state','property__description','value','last_modified')
    list_filter = ('material_version', 'last_modified')

class MaterialVersionAdmin(BaseAdmin):
    list_display  = ('material','version','grade','notes')
    list_filter = ('material', 'grade')
    search_fields = ('material__name','version','grade','notes')
    exclude = ('version_value',)
    #save_as = True

class MaterialPropertyAdmin(BaseAdmin):
    list_display  = ('name','description','unit','state')
    list_filter = ('state', 'last_modified')
    search_fields = ('name','description','unit','state')
    
admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialVersion, MaterialVersionAdmin)
admin.site.register(VariableProperty, VariablePropertyAdmin)
admin.site.register(ConstProperty, ConstPropertyAdmin)
admin.site.register(MatrixProperty, MatrixPropertyAdmin)

