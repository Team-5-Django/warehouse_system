from django.shortcuts import render

from inventory.models import Category, Product
from orders.models import Order , Supermarket
from shipments.models import Shipment ,Factory
from users.models import User

def get_dashboard_page(request):
    users = User.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    orders = Order.objects.all()    
    supermarkets = Supermarket.objects.all()
    factories = Factory.objects.all()
    shipments = Shipment.objects.all()


    return render(request, 'dashboard.html', {'users': users, 'products': products, 'categories': categories, 'orders': orders, 'shipments': shipments, 'supermarkets': supermarkets, 'factories': factories})
