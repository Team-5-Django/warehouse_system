from django import forms
from django.forms import inlineformset_factory
from .models import Shipment, ShipmentLineItem ,Factory

class ShipmentForm(forms.ModelForm):
    factory = forms.ModelChoiceField(
        queryset=Factory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="-- Select Factory --"
    )
    class Meta:
        model = Shipment
        fields = ['reference', 'factory', 'status']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reference'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ShipmentLineItemForm(forms.ModelForm):
    class Meta:
        model = ShipmentLineItem
        fields = ['product', 'quantity']

ShipmentLineItemFormSet = inlineformset_factory(
    Shipment, ShipmentLineItem,
    form=ShipmentLineItemForm,
    extra=1,
    can_delete=False
)



