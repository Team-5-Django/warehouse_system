from django import forms 
from .models import Product , Category 

class productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ['sku','created_at', 'updated_at','status']


class categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"



