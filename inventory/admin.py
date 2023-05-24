from django.contrib import admin
from .models import Material, MaterialGroup, MaterialStorage, MaterialStorageWithdraw


@admin.register(MaterialGroup)
class MaterialGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'group']


@admin.register(MaterialStorage)
class MaterialStorageAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'item', 'purchase_date', 'expiration_date', 
        'unit_cost', 'unit_amount', 'total_cost', 'current_amount',
        'withdraw_amount'
    ]



@admin.register(MaterialStorageWithdraw)
class MaterialStorageWithdrawAdmin(admin.ModelAdmin):
    list_display = ['id', 'storage', 'unit_amount', 'withdraw_date']
