from django.contrib import admin
from .models import Material, MaterialVersion, VariableProperties, ConstProperty, MatrixProperty

# Register your models here
class ConstPropertyAdmin(admin.ModelAdmin):
    list_display= ('name', 'material','state', 'value', 'description', 'last_modified')
    list_filter = ('material', 'state', 'last_modified')
    search_fields = ('name', 'material__material__name','material__version','state', 'value', 'description', 'last_modified')

class MaterialAdmin(admin.ModelAdmin):
    list_display= ('name','description')
    search_fields = ('name','description')

class MaterialVersionAdmin(admin.ModelAdmin):
    list_display  = ('material','version','grade','notes','date')
    list_filter = ('material', 'grade')
    search_fields = ('material__name','version','grade','notes','date')

class VariablePropertiesAdmin(admin.ModelAdmin):
    list_display  = ('material','state','references','last_modified')
    search_fields = ('material__material__name','state','references','last_modified')
    list_filter = ('material', 'state', 'last_modified')

class MatrixPropertyAdmin(admin.ModelAdmin):
    list_display = ('name','material','state','description','value','last_modified')
    search_fields = ('name','material__material__name','material__version','state','description','value','last_modified')
    list_filter = ('material', 'state', 'last_modified')

admin.site.register(Material,MaterialAdmin)
admin.site.register(MaterialVersion,MaterialVersionAdmin)
admin.site.register(VariableProperties,VariablePropertiesAdmin)
admin.site.register(ConstProperty, ConstPropertyAdmin)
admin.site.register(MatrixProperty,MatrixPropertyAdmin)

