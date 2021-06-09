from django.contrib import admin

# Register your models here.
from .models import BaseUnit, BaseUnitPower, ComboUnit, BaseUnitPrefix, AlternateUnitSymbol
from .models import UnitSystem

class BaseUnitInline(admin.TabularInline):
    model = BaseUnitPower
    extra = 0

class AlternateSymbolInline(admin.TabularInline):
    model = AlternateUnitSymbol
    extra = 0

class ComboAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')
    inlines = [
        BaseUnitInline,
        AlternateSymbolInline,
    ]

class BaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')

class PrefixAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'value')

class UnitSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(BaseUnit, BaseAdmin)
admin.site.register(ComboUnit,ComboAdmin)
admin.site.register(BaseUnitPrefix,PrefixAdmin)
admin.site.register(UnitSystem, UnitSystemAdmin)