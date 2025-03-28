# Generated by Django 5.1.7 on 2025-03-24 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('thumbnail', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('sku', models.CharField(blank=True, max_length=50, null=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('critical_quantity', models.PositiveIntegerField(default=10)),
                ('thumbnail', models.URLField(blank=True, default='https://mmi-global.com/wp-content/uploads/2020/05/default-product-image.jpg', null=True)),
                ('status', models.CharField(choices=[('in_stock', 'In Stock'), ('low_stock', 'Low Stock'), ('out_of_stock', 'Out of Stock')], default='in_stock', max_length=20)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
            ],
        ),
    ]
