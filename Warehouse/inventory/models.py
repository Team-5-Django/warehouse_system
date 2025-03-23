from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"

    STOCK_CHOICES = [
        (IN_STOCK, "In Stock"),
        (LOW_STOCK, "Low Stock"),
        (OUT_OF_STOCK, "Out of Stock"),
    ]
    name = models.CharField(max_length=100)
    factory=models.ForeignKey('shipments.Factory',on_delete=models.DO_NOTHING ,null=True ,blank=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, blank=True,null=True)
    quantity = models.PositiveIntegerField(default=0)
    critical_quantity = models.PositiveIntegerField(default=10)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)

    thumbnail = models.URLField(null=True, blank=True, default='https://mmi-global.com/wp-content/uploads/2020/05/default-product-image.jpg')
    status = models.CharField(max_length=20, choices=STOCK_CHOICES, default="in_stock")
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on each save
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
            constraints = [
                UniqueConstraint(fields=['name', 'category'], name='unique_name_category')
            ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def is_low_stock(self):
      
        return self.quantity <= self.critical_quantity

    def is_out_of_stock(self):
       
        return self.quantity == 0

    def update_stock_status(self):
        # Update the status based on current stock levels
        if self.is_out_of_stock():
            self.status = self.OUT_OF_STOCK
        elif self.is_low_stock():
            self.status = self.LOW_STOCK
        else:
            self.status = self.IN_STOCK
    def set_sku(self):
        if not self.sku:
            self.sku = f"{self.name.upper()}-{str(self.category).upper()}"
    def clean(self):
        if self.quantity < 0:
            raise ValidationError("Stock quantity cannot be negative!")
        if self.pk is None and self.quantity <= self.critical_quantity:
            raise ValidationError("Stock quantity must be greater than critical quantity.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        self.set_sku()
        super().save(*args, **kwargs)
