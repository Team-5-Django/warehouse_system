from django import forms 
from .models import Product , Category 

class productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"



