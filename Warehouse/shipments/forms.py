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
        fields = ['reference', 'factory']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter reference'}),
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

class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        fields = '__all__'
        


