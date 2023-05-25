from django.db import models
from inventory.models import CurrencyField
from decimal import Decimal


class Client(models.Model):
    name = models.CharField(max_length=128)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    street = models.CharField(max_length=64, blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    number = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    # score = models.PositiveSmallIntegerField()


class ProductCategory(models.Model):
    description = models.CharField(max_length=64)


class Product(models.Model):
    description = models.CharField(max_length=64)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    combo = models.ManyToManyField('self', through='ProductCombo', blank=True)
    cost = CurrencyField()
    notes = models.TextField(blank=True, null=True)
    recipe = models.TextField(blank=True, null=True)

    @property
    def suggested_value(self):
        value = 0
        for product_combo in self.combo.through.objects.filter(main_product_id=self.id):
            value += product_combo.sub_total
        return value
        
    def __str__(self):
        return self.description

class ProductCombo(models.Model):
    main_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='combo_main_products')
    sub_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='combo_sub_products')
    unit_amount = models.PositiveSmallIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default='0.00')
    @property
    def sub_total(self):
        return round((self.sub_product.cost - (self.sub_product.cost * (self.discount / Decimal('100')))) * self.unit_amount, 2)
    
class ProductMenu(models.Model):
    description = models.CharField(max_length=64)
    products = models.ManyToManyField(Product, through='ProductOption')

    def __str__(self):
        return self.description


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    menu = models.ForeignKey(ProductMenu, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    sequence = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.product.description} | {self.final_cost}'

    @property
    def final_cost(self):
        return round(self.product.cost - (self.product.cost * (self.discount / 100)), 2)


class Order(models.Model):
    product_orders = models.ManyToManyField(ProductOption, through='ProductOrder')
    table_number = models.PositiveSmallIntegerField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    menu = models.ForeignKey(ProductMenu, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()
    
    @property
    def total_cost(self):
        value = Decimal('0.00')
        orders = self.product_orders.through.objects.filter(order_id=self.id)
        for product_order in orders:
            value += product_order.sub_total
        return value


class ProductOrder(models.Model):
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit_amount = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    sub_total = CurrencyField(editable=False)

    def save(self):
        self.sub_total = self.product_option.final_cost * self.unit_amount
        return super().save()
