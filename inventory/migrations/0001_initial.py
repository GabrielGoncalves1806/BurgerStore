# Generated by Django 4.2.1 on 2023-05-25 02:37

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import inventory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='MaterialStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(choices=[('UND', 'UND'), ('KG', 'KG'), ('L', 'L'), ('CX', 'CX')], max_length=10)),
                ('unit_cost', inventory.models.CurrencyField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('unit_amount', inventory.models.AmountField(decimal_places=3, default=Decimal('0.000'), max_digits=10)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('purchase_date', models.DateField(auto_now_add=True)),
                ('observation', models.TextField(blank=True, null=True)),
                ('allow_negative', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.material')),
            ],
        ),
        migrations.CreateModel(
            name='MaterialStorageWithdraw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_amount', inventory.models.AmountField(decimal_places=3, default=Decimal('0.000'), max_digits=10)),
                ('withdraw_date', models.DateField(default=django.utils.timezone.now)),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdraws', to='inventory.materialstorage')),
            ],
        ),
        migrations.AddField(
            model_name='material',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.materialgroup'),
        ),
    ]
