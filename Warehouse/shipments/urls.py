from django.urls import path
from .views import shipment_list, shipment_detail, add_shipment, edit_shipment, confirm_shipment,remove_shipment_item,delete_shipment

urlpatterns = [
    path('', shipment_list, name='shipment_list'),
    path('<int:shipment_id>/', shipment_detail, name='shipment_detail'),
    path('add/', add_shipment, name='add_shipment'),
    path('<int:shipment_id>/edit/', edit_shipment, name='edit_shipment'),
    path('<int:shipment_id>/confirm/', confirm_shipment, name='confirm_shipment'),
    path('remove_item/<int:item_id>/', remove_shipment_item, name='remove_shipment_item'),
    path('shipments/<int:shipment_id>/delete/', delete_shipment, name='delete_shipment'),

]
