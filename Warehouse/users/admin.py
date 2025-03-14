from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from inventory.models import Product, Category
from orders.models import Order, OrderLineItem
from shipments.models import Shipment, ShipmentLineItem
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Shipment)       
admin.site.register(ShipmentLineItem)

