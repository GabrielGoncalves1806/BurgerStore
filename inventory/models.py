from django.db import models


class CurrencyField(models.DecimalField):

    MAX_DIGITS = 10
    DECIMAL_PLACES = 2

    def __init__(self, verbose_name=None, name=None, **kwargs,):
        kwargs.update({"max_digits": CurrencyField.MAX_DIGITS})
        kwargs.update({"decimal_places": CurrencyField.DECIMAL_PLACES})
        super().__init__(verbose_name, name, **kwargs)


class MaterialGroup(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.description

class Material(models.Model):
    description = models.CharField(max_length=64)
    group = models.ForeignKey(MaterialGroup, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.group:
            return f'{self.group} | {self.description}'
        return self.description


class MaterialStorage(models.Model):
    
    UNIT_TYPES = (
        ('UND', 'UND'),
        ('KG', 'KG'),
        ('CX', 'CX'),
    )
    
    item = models.ForeignKey(Material, on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=10, choices=UNIT_TYPES)
    unit_cost = CurrencyField()
    unit_amount = models.PositiveSmallIntegerField()
    expiration_date = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(auto_now_add=True)
    observation = models.TextField(blank=True, null=True)

    @property
    def total_cost(self):
        return self.unit_cost * self.unit_amount