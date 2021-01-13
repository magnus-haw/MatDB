from django.contrib import admin
from .models import Person

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display= ('name', 'email','phone', 'affiliation', 'office', 'last_modified')
    list_filter = ('affiliation', 'last_modified')
    search_fields = ('name', 'email','phone','affiliation', 'office', 'notes', 'last_modified')
    readonly_fields = ['last_modified', 'created_at']

admin.site.register(Person,PersonAdmin)