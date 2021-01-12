from django.contrib import admin

# Register your models here.
from .models import BaseUnit, BaseUnitPower, ComboUnit

class BaseUnitInline(admin.TabularInline):
    model = BaseUnitPower
    extra = 0

class ComboAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')
    inlines = [
        BaseUnitInline,
    ]

class BaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')

admin.site.register(BaseUnit, BaseAdmin)
admin.site.register(ComboUnit,ComboAdmin)