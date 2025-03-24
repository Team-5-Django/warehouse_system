from django.urls import path 
from .views import DashboardView, ProductsListView #get_dashboard_page

urlpatterns = [
    # path('', get_dashboard_page, name='dashboard')
    path('', DashboardView.as_view(), name='dashboard'),
    path('products-list', ProductsListView.as_view(), name='products-list'),
]
