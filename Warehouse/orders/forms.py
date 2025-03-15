from django import forms
from .models import Order, OrderLineItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['reference', 'supermarket', 'status']

class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ['product', 'quantity', 'price']

OrderLineItemFormSet = forms.inlineformset_factory(
    Order, OrderLineItem, form=OrderLineItemForm, extra=1, can_delete=True
)