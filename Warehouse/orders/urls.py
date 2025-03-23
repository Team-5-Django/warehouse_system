from django.urls import path
from .views import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView,Confirm_order_view,shipping_order_view,delivery_order_view,cancel_order_view, SupermarketListView, SupermarketCreateView, SupermarketUpdateView, SupermarketDeleteView

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),

    path('confirm/<int:pk>', Confirm_order_view, name='confirm_order'),
    path('shipping/<int:pk>', shipping_order_view, name='shipping_order'),
    path('delivered/<int:pk>', delivery_order_view, name='delivered_order'),
    path('cancelled/<int:pk>', cancel_order_view, name='cancel_order'),


    path('supermarkets/', SupermarketListView.as_view(), name='supermarket_list'),
    path('supermarkets/create/', SupermarketCreateView.as_view(), name='supermarket_create'),
    path('supermarkets/<int:pk>/update/', SupermarketUpdateView.as_view(), name='supermarket_update'),
    path('supermarkets/<int:pk>/delete/', SupermarketDeleteView.as_view(), name='supermarket_delete'),

]