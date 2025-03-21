from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from inventory.models import Product, Category
from orders.models import Order, OrderLineItem, Supermarket
from shipments.models import Factory, Shipment, ShipmentLineItem
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Order)
admin.site.register(Shipment)       
admin.site.register(ShipmentLineItem)
admin.site.register(Factory)

