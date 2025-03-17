# orders/forms.py
from django import forms
from .models import Order, OrderLineItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['reference', 'supermarket', 'status']
        widgets = {
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'supermarket': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

OrderLineItemFormSet = forms.inlineformset_factory(
    Order,
    OrderLineItem,
    form=OrderLineItemForm,
    extra=1,
    can_delete=True,
    widgets={
        'DELETE': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
)