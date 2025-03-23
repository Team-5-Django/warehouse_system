from django.db import transaction
from django.core.exceptions import ValidationError
from inventory.models import Product


@transaction.atomic
def mark_shipment_as_delivered(shipment):
    if shipment.status == 'Delivered':
        raise ValidationError("This shipment has already been delivered.")

    for item in shipment.line_items.all():
        product = Product.objects.select_for_update().get(id=item.product.id)
        product.quantity += item.quantity
        product.save()

    shipment.status = 'Delivered'
    shipment.save()