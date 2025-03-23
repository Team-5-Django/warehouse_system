from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product

@receiver(pre_save, sender=Product)
def update_status(sender, instance, **kwargs):
    instance.update_stock_status()
