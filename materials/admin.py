from django.contrib import admin
from .models import Material, MaterialVersion, VariableProperties, ConstProperty, MatrixProperty

# Register your models here
class ConstPropertyAdmin(admin.ModelAdmin):
    list_display= ('name', 'material','state', 'value', 'description', 'last_modified')
    list_filter = ('material', 'state', 'last_modified')

class MaterialAdmin(admin.ModelAdmin):
    list_display= ('name','description')

class MaterialVersionAdmin(admin.ModelAdmin):
    list_display= ('material','version','rating','notes','date')

admin.site.register(Material,MaterialAdmin)
admin.site.register(MaterialVersion,MaterialVersionAdmin)
admin.site.register(VariableProperties)
admin.site.register(ConstProperty, ConstPropertyAdmin)
admin.site.register(MatrixProperty)

