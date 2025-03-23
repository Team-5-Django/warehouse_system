from django import forms
from .models import Order, OrderLineItem, Supermarket
from django.utils.safestring import mark_safe

class DeleteButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        return mark_safe(f'<button type="button" class="btn btn-danger delete-button" data-name="{name}">Delete</button>')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['supermarket', 'status']
        widgets = {
            'supermarket': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select', 'onchange': 'updateMaxQuantity(this)'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control quantity_input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._configure_product_field()

    def _configure_product_field(self):
        product_field = self.fields.get('product')
        if product_field and hasattr(product_field, 'queryset'):
            product_field.choices = [('', 'Select a product')] + [
                (choice.pk, f"{choice.name} (Stock: {choice.quantity})")
                for choice in product_field.queryset
            ]
            product_field.widget.attrs.update({
                'class': 'form-select',
                'data-stock': 'stock-value',
                'default': '------'
            })

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')
        if product and quantity and product.quantity < quantity:
            self.add_error('quantity', 'Quantity exceeds stock.')
        return quantity

OrderLineItemFormSet = forms.inlineformset_factory(
    Order,
    OrderLineItem,
    form=OrderLineItemForm,
    extra=1,
    can_delete=True,

)

class SupermarketForm(forms.ModelForm):
    class Meta:
        model = Supermarket
        fields = ['name', 'address', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }