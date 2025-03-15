from django.shortcuts import render ,redirect , get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView , CreateView , UpdateView , DeleteView
from .models import *
from .forms import productform , categoryform



def products(request):
    products = Product.objects.all()  
    return render(request, 'inventory/products.html', {'products': products})

class productdetails(DetailView):
    model = Product
    template_name ="inventory/productdetails.html"
    context_object_name = "product"
    pk_url_kwarg = "product_id"


class CategoryListView(ListView):
   model = Category
   template_name = "inventory/categories.html"
   context_object_name = "categories"


def category_products(request, category_id): 
    category = get_object_or_404(Category, id=category_id) 
    products = Product.objects.filter(category=category)  
    return render(request, 'inventory/category_products.html', {'category': category, 'products': products})

class ProductCreateView(CreateView):
    model = Product
    template_name = "inventory/forms/form.html"
    form_class = productform
    success_url = "/products/"



class ProductDeleteView(DeleteView):
    model = Product
    template_name = "inventory/confirm_delete.html" 
    success_url = reverse_lazy("products") 



class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "inventory/confirm_delete.html"  
    success_url = reverse_lazy("categoryproducts") 





class ProductUpdateView(UpdateView):
    model = Product
    template_name = "inventory/forms/form.html"
    form_class = productform

    def get_success_url(self):
        return reverse_lazy("productdetails", kwargs={"product_id": self.object.id})
    




class CategoryCreateView(CreateView):
    model = Category
    template_name = "inventory/forms/form.html"
    form_class = categoryform
    success_url = "/inventory/category/"









