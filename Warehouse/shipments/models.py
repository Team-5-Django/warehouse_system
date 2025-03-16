from django.db import models
from users.models import User
from inventory.models import Product

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    reference = models.CharField(max_length=100, unique=True)
    factory = models.ForeignKey('Factory', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        ordering = ['status', '-created_at']
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"

    def __str__(self):
        return f"{self.reference} - {self.status}"

class Factory(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

class ShipmentLineItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='line_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Shipment: {self.shipment.reference})"



from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
#from .models import ShipmentLineItem
#from inventory.models import Product

@receiver(post_save, sender=ShipmentLineItem)
def update_product_quantity_on_add(sender, instance, created, **kwargs):
    if created:
        instance.product.quantity += instance.quantity
        instance.product.save()

@receiver(post_delete, sender=ShipmentLineItem)
def update_product_quantity_on_delete(sender, instance, **kwargs):
    instance.product.quantity -= instance.quantity
    instance.product.save()

