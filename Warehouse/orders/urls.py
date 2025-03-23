from django.urls import path
from .views import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView,Confirm_order_view,shipping_order_view,delivery_order_view,cancel_order_view

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),

    path('confirm/<int:pk>', Confirm_order_view, name='confirm_order'),
    path('shipping/<int:pk>', shipping_order_view, name='shipping_order'),
    path('delivered/<int:pk>', delivery_order_view, name='delivered_order'),
    path('cancelled/<int:pk>', cancel_order_view, name='cancel_order'),


    

]