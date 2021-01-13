from django.contrib import admin
from .models import Material, MaterialVersion, VariableProperties
from .models import ConstProperty, MatrixProperty, Reference

# Register your models here
class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at','last_modified','modified_by',]

    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        print(obj.modified_by)
        super().save_model(request, obj, form, change)

class ConstPropertyAdmin(BaseAdmin):
    list_display= ('name', 'material','state', 'value', 'description', 'last_modified')
    list_filter = ('material', 'state', 'last_modified')
    search_fields = ('name', 'material__material__name','material__version','state', 'value', 'description', 'last_modified')
    
class MaterialAdmin(BaseAdmin):
    list_display= ('name','description')
    search_fields = ('name','description')

class VariablePropertiesAdmin(BaseAdmin):
    list_display  = ('material','state','last_modified')
    search_fields = ('material__material__name','state','last_modified')
    list_filter = ('material', 'state', 'last_modified')

class MatrixPropertyAdmin(BaseAdmin):
    list_display = ('name','material','state','description','value','last_modified')
    search_fields = ('name','material__material__name','material__version','state','description','value','last_modified')
    list_filter = ('material', 'state', 'last_modified')

class ReferenceAdmin(BaseAdmin):
    list_display = ('title','material','published','last_modified')
    search_fields = ('title','material__material__name','material__version','body','published','last_modified')
    list_filter = ('material', 'last_modified')

class ReferenceInline(admin.StackedInline):
    model = Reference
    extra = 0
    readonly_fields = ['created_at','last_modified','modified_by',]

class MaterialVersionAdmin(BaseAdmin):
    list_display  = ('material','version','grade','notes')
    list_filter = ('material', 'grade')
    search_fields = ('material__name','version','grade','notes')
    inlines = [
        ReferenceInline,
    ]

admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialVersion, MaterialVersionAdmin)
admin.site.register(VariableProperties, VariablePropertiesAdmin)
admin.site.register(ConstProperty, ConstPropertyAdmin)
admin.site.register(MatrixProperty, MatrixPropertyAdmin)
admin.site.register(Reference, ReferenceAdmin)

