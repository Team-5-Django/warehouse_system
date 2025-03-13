from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    critical_quantity = models.PositiveIntegerField(default=10)
    category=models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def is_low_stock(self):
        return self.quantity <= self.critical_quantity

    def is_out_of_stock(self):
        return self.quantity == 0

