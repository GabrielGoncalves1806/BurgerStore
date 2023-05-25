from django.db import models
from django.utils import timezone
from django.forms import ValidationError
from decimal import Decimal, getcontext


class CurrencyField(models.DecimalField):

    MAX_DIGITS = 10
    DECIMAL_PLACES = 2

    def __init__(self, verbose_name=None, name=None, default=Decimal('0.00'), **kwargs):
        kwargs.update({"max_digits": CurrencyField.MAX_DIGITS})
        kwargs.update({"decimal_places": CurrencyField.DECIMAL_PLACES})
        super().__init__(verbose_name, name, default=default, **kwargs)


class AmountField(models.DecimalField):

    MAX_DIGITS = 10
    DECIMAL_PLACES = 3

    def __init__(self, verbose_name=None, name=None, default=Decimal('0.000'), **kwargs,):
        kwargs.update({"max_digits": AmountField.MAX_DIGITS})
        kwargs.update({"decimal_places": AmountField.DECIMAL_PLACES})
        super().__init__(verbose_name, name, default=default, **kwargs)


class MaterialGroup(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):
        return self.description


class Material(models.Model):
    description = models.CharField(max_length=64)
    group = models.ForeignKey(
        MaterialGroup, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.group:
            return f'{self.group} | {self.description}'
        return self.description


class MaterialStorage(models.Model):

    UNIT_TYPES = (
        ('UND', 'UND'),
        ('KG', 'KG'),
        ('L', 'L'),
        ('CX', 'CX'),
    )

    item = models.ForeignKey(Material, on_delete=models.CASCADE)
    unit_type = models.CharField(max_length=10, choices=UNIT_TYPES)
    unit_cost = CurrencyField()
    unit_amount = AmountField()
    expiration_date = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(auto_now_add=True)
    observation = models.TextField(blank=True, null=True)
    allow_negative = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.item} | {self.unit_cost} | {self.purchase_date}'

    @property
    def total_cost(self):
        return round(self.unit_cost * self.unit_amount, 2)

    @property
    def current_amount(self):
        return self.unit_amount - self.withdraw_amount

    @property
    def withdraw_amount(self):
        amount = 0
        for withdraw in self.withdraws.all():
            amount += withdraw.unit_amount
        return amount


class MaterialStorageWithdraw(models.Model):
    storage = models.ForeignKey(
        MaterialStorage, on_delete=models.CASCADE, related_name='withdraws')
    unit_amount = AmountField()
    withdraw_date = models.DateField(default=timezone.now)

    def save(self):
        self.clean()
        return super().save()

    def validate_amount(self, errors):
        if self.storage.allow_negative:
            return
        if self.unit_amount > self.storage.current_amount:
            unit_error = f'Storage amount is {self.storage.current_amount} and cannot be negative.'
            errors.update({'unit_amount': unit_error})

    def clean(self):
        errors = {}
        self.validate_amount(errors)
        if errors:
            raise ValidationError(errors)
        return super().clean()
