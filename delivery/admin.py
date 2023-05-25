from typing import Any, List, Optional
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.http.request import HttpRequest

from .models import Client, Order, Product, ProductCategory, ProductMenu, ProductOption


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    readonly_fields = ['final_cost']
    extra = 0

class ProductOptionOrderInline(admin.TabularInline):
    model = Order.product_orders.through
    readonly_fields = ['sub_total']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        order = request.GET.get('obj', None)
        if db_field.name == "product_option":
            product_options = ProductOption.objects.all()
            if order and order.menu:
                product_options = product_options.filter(menu=order.menu)
                
            kwargs["queryset"] = product_options
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class ProductComboInline(admin.TabularInline):
    model = Product.combo.through
    extra = 0
    fk_name = 'main_product'
    readonly_fields = ['sub_total']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductOptionOrderInline]
    readonly_fields = ['total_cost', 'created_at']
    
    
    def get_inline_instances(self, request, obj):
        request.GET._mutable = True
        request.GET.update({'obj': obj})
        inlines = super().get_inline_instances(request, obj)
        return inlines
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'cost']
    readonly_fields = ['suggested_value']
    inlines = [ProductComboInline]

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductMenu)
class ProductMenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'description']
    inlines = [ProductOptionInline]
    
    
@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    pass
