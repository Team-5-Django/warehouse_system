from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    STOCK_CHOICES = [
        ("in_stock", "In Stock"),
        ("low_stock", "Low Stock"),
        ("out_of_stock", "Out of Stock"),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField(default=0)
    critical_quantity = models.PositiveIntegerField(default=10)
    category=models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    thumbnail = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STOCK_CHOICES, default="in_stock")


    def __str__(self):
        return f"{self.name} ({self.sku})"

    def is_low_stock(self):
      
        return self.quantity <= self.critical_quantity

    def is_out_of_stock(self):
       
        return self.quantity == 0

    def update_stock_status(self):
        
        if self.is_out_of_stock():
            self.status = "out_of_stock"
        elif self.is_low_stock():
            self.status = "low_stock"
        else:
            self.status = "in_stock"

    def save(self, *args, **kwargs):
        self.update_stock_status()
        super().save(*args, **kwargs)
