from django.contrib import admin
from .models import Order,OrderLineItem, Supermarket

# Register your models here.
#view the orderlineitem as a subclass of Order
@admin.register(OrderLineItem)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__reference', 'product__name')


admin.site.register(Supermarket)

