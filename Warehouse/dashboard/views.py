from django.shortcuts import render
from django.views.generic import TemplateView
from inventory.models import Category, Product
from orders.models import Order , Supermarket
from shipments.models import Shipment ,Factory
from users.models import User
from django.db.models import Count  


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
        products_count = Product.objects.values_list("name", "quantity")
        factory_shipment = Factory.objects.annotate(total_shipments=Count('shipments')).values('name', 'total_shipments')
        supermarket_order = Supermarket.objects.annotate(total_orders=Count('orders')).values('name', 'total_orders')

        context.update({
            'users': users,
            'products': products,
            'categories': categories,
            'orders': orders,
            'factories':factories,
            'supermarkets': supermarkets,
            'shipments': shipments,
            'products_count': list(products_count),
            "factory_shipment" : list(factory_shipment),
            "supermarket_order" : list(supermarket_order),
        })

        return context

