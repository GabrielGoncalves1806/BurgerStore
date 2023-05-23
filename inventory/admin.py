from django.contrib import admin
from .models import Material, MaterialGroup, MaterialStorage


@admin.register(MaterialGroup)
class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'group']


@admin.register(MaterialStorage)
class MaterialStorageAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'purchase_date', 'expiration_date', 'unit_cost', 'unit_amount', 'total_cost']
    
    def total_cost(self, obj):
        return obj.total_cost