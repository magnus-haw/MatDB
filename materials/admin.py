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
    list_display= ('name', 'material_version','state', 'value', 'unit','description', 'last_modified')
    list_filter = ('material_version', 'state', 'last_modified')
    search_fields = ('name', 'material_version__material__name','material_version__version','state', 'value', 'description', 'last_modified')
    
class MaterialAdmin(BaseAdmin):
    list_display= ('name','short_description')
    search_fields = ('name','description')

# class VariablePropertiesAdmin(BaseAdmin):
#     list_display  = ('material_version','state','last_modified')
#     search_fields = ('material_version__material__name','state','last_modified')
#     list_filter = ('material_version', 'state', 'last_modified')

class VariablePropertyAdmin(BaseAdmin):
    list_display  = ('name','material_version','state','unit','last_modified')
    search_fields = ('name','material_version__material__name','state','last_modified')
    list_filter = ('material_version', 'state', 'last_modified')

class MatrixPropertyAdmin(BaseAdmin):
    list_display = ('name','material_version','state','description','value','last_modified')
    search_fields = ('name','material_version__material__name','material_version__version','state','description','value','last_modified')
    list_filter = ('material_version', 'state', 'last_modified')

class MaterialVersionAdmin(BaseAdmin):
    list_display  = ('material','version','grade','notes')
    list_filter = ('material', 'grade')
    search_fields = ('material__name','version','grade','notes')
    #save_as = True

admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialVersion, MaterialVersionAdmin)
# admin.site.register(VariableProperties, VariablePropertiesAdmin)
admin.site.register(VariableProperty, VariablePropertyAdmin)
admin.site.register(ConstProperty, ConstPropertyAdmin)
admin.site.register(MatrixProperty, MatrixPropertyAdmin)

