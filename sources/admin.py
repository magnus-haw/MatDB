from django.contrib import admin

from materials.admin import BaseAdmin
from .models import Person, Reference, Tutorial

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display= ('name', 'email','phone', 'affiliation', 'office', 'last_modified')
    list_filter = ('affiliation', 'last_modified')
    search_fields = ('name', 'email','phone','affiliation', 'office', 'notes', 'last_modified')
    readonly_fields = ['last_modified', 'created_at']

class TutorialAdmin(BaseAdmin):
    list_display= ('name', 'link', 'last_modified', 'short_description')
    list_filter = ('last_modified',)
    search_fields = ('name','link','softwares','materials','description','last_modified', 'short_description')

class ReferenceAdmin(BaseAdmin):
    list_display = ('title','authors','published','last_modified')
    search_fields = ('title','authors','body','published','last_modified')
    list_filter = ('last_modified',)

admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(Reference,ReferenceAdmin)