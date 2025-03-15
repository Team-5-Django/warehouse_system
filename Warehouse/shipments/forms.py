from django import forms
from django.forms import inlineformset_factory
from .models import Shipment, ShipmentLineItem

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['reference', 'factory', 'status']

class ShipmentLineItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentLineItem
        fields = ['product', 'quantity']

ShipmentLineItemFormSet = inlineformset_factory(
    Shipment, ShipmentLineItem,
    form=ShipmentLineItemForm,
    extra=0,
    can_delete=False
)

