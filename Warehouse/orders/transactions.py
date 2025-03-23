from django.db import transaction
from django.core.exceptions import ValidationError
from inventory.models import Product

@transaction.atomic
def process_order(order):
    for item in order.line_items.all():
        product = Product.objects.select_for_update().get(id=item.product.id)
        
        if product.quantity < item.quantity:
            raise ValidationError(
                f"Insufficient stock for {product.name}. Available: {product.quantity}, Required: {item.quantity}"
            )
        
        product.quantity -= item.quantity
        product.save()
    
    order.status = 'Confirmed'
    order.save()
# shipping

