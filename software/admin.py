from django.contrib import admin
from materials.admin import BaseAdmin
from .models import Software, SoftwareVersion, Tutorial
from .models import ExportFormat

# Register your models here

class SoftwareAdmin(BaseAdmin):
    list_display= ('name', 'short_name','short_description','last_modified')
    list_filter = ('last_modified',)
    search_fields = ('name', 'short_name','description','how_to_get', 'how_to_use', 'point_of_contact', 'last_modified')

class SoftwareVersionAdmin(BaseAdmin):
    list_display= ('software', 'version', 'last_modified', 'short_description')
    list_filter = ('software', 'last_modified',)
    search_fields = ('software', 'software__name','software__short_name','short_description', 'software__description', 'last_modified')

class ExportFormatAdmin(BaseAdmin):
    list_display= ('material_version', 'software_version','last_modified')
    list_filter = ('last_modified',)
    search_fields = ('material_version', 'software_version','description','last_modified')

class TutorialAdmin(BaseAdmin):
    list_display= ('name', 'link', 'software_version','last_modified', 'short_description')
    list_filter = ('software_version','last_modified',)
    search_fields = ('name','link','software_version','description','last_modified', 'short_description')

admin.site.register(Software, SoftwareAdmin)
admin.site.register(SoftwareVersion, SoftwareVersionAdmin)
admin.site.register(ExportFormat, ExportFormatAdmin)
admin.site.register(Tutorial, TutorialAdmin)