from django.shortcuts import render
from django.views.generic import TemplateView
from inventory.models import Category, Product
from orders.models import Order , Supermarket
from shipments.models import Shipment ,Factory
from users.models import User

# def get_dashboard_page(request):
#     users = User.objects.all()
#     products = Product.objects.all()
#     categories = Category.objects.all()
#     orders = Order.objects.all()    
#     supermarkets = Supermarket.objects.all()
#     factories = Factory.objects.all()
#     shipments = Shipment.objects.all()

#     context = {
#         'users': users,
#         'products': products,
#         'categories': categories,
#         'orders': orders,
#         'supermarkets': supermarkets,
#         'factories': factories,
#         'shipments': shipments,
#     }

#     return render(request, 'dashboard.html', context)

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        products = Product.objects.all()
        categories = Category.objects.all()
        orders = Order.objects.all()    
        supermarkets = Supermarket.objects.all()
        factories = Factory.objects.all()
        shipments = Shipment.objects.all()

        context = {
        'users': users,
        'products': products,
        'categories': categories,
        'orders': orders,
        'supermarkets': supermarkets,
        'factories': factories,
        'shipments': shipments,
        }

        products = Product.objects.values_list("name", "quantity")
        context['products_count'] = list(products)

        return context
