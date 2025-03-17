from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from orders.models import Order, OrderLineItem
from shipments.models import Shipment, ShipmentLineItem
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Order)
admin.site.register(Shipment)       
admin.site.register(ShipmentLineItem)

