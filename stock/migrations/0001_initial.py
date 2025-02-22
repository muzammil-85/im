# Generated by Django 4.2.18 on 2025-02-17 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('shopname', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('vehicle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('vehicle_no', models.CharField(max_length=50)),
                ('license_no', models.CharField(max_length=50)),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('piece_per_box', models.IntegerField(default=0)),
                ('mrp', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('shopname', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SupplierOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('item_expiry_date', models.DateField(null=True)),
                ('total_qty', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_driver', to='stock.driver')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_orders', to='stock.item')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='stock.supplier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'supplier_order',
            },
        ),
        migrations.CreateModel(
            name='SupplierItemPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Discount', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_prices', to='stock.item')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplier_prices', to='stock.supplier')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(auto_created=True, auto_now=True)),
                ('date', models.DateField()),
                ('item_date', models.DateField()),
                ('total_qty', models.IntegerField(editable=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_entries', to='stock.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'stock',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt_no', models.CharField(max_length=20, unique=True)),
                ('date', models.DateField()),
                ('customer_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_no', models.CharField(max_length=20, unique=True)),
                ('date', models.DateField()),
                ('customer_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('item_expiry_date', models.DateField(null=True)),
                ('total_qty', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='stock.customer')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_driver', to='stock.driver')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_orders', to='stock.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'customer_order',
            },
        ),
        migrations.CreateModel(
            name='CustomerItemPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('Discount', models.IntegerField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_prices', to='stock.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_prices', to='stock.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
