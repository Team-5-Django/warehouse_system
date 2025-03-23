from django.db import models
from users.models import User
from inventory.models import Product


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
    ]

    reference = models.CharField(max_length=100, unique=True)
    factory = models.ForeignKey('Factory', on_delete=models.SET_NULL, null=True, related_name='shipments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        ordering = ['status', '-created_at']
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
        permissions = [
            ('confirm_shipment', 'Can confirm shipment'),
            ('deliver_shipment', 'Can deliver shipment'),
        ]

    def __str__(self):
        return f"{self.reference} - {self.status}"


class Factory(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def total_shipments(self):
        return self.shipments.count()


class ShipmentLineItem(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='line_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Shipment: {self.shipment.reference})"