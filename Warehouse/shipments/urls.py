from django.urls import path
from .views import (shipment_list, 
                    shipment_detail, 
                    add_shipment, 
                    edit_shipment, 
                    confirm_shipment,
                    delivered_shipment,
                    remove_shipment_item,
                    cancel_shipment,
                    factory_list,
                    factory_detail,
                    edit_factory,
                    delete_factory,
                    add_factory

                    )
urlpatterns = [
    path('', shipment_list, name='shipment_list'),
    path('<int:shipment_id>/', shipment_detail, name='shipment_detail'),
    path('add/', add_shipment, name='add_shipment'),
    path('<int:shipment_id>/edit/', edit_shipment, name='edit_shipment'),
    path('<int:shipment_id>/confirm/', confirm_shipment, name='confirm_shipment'),
    path('remove_item/<int:item_id>/', remove_shipment_item, name='remove_shipment_item'),
    path('shipments/<int:shipment_id>/delete/', cancel_shipment, name='cancle_shipment'),
    path('shipments/<int:shipment_id>/delivered/', delivered_shipment, name='delivered_shipment'),
# factory urls
    path('factory_list/', factory_list, name='factory_list'),
    path('factory/<int:factory_id>/', factory_detail, name='factory_detail'),
    path('factory/add/', add_factory, name='add_factory'),
    path('factory/<int:factory_id>/edit/', edit_factory, name='edit_factory'),
    path('factory/<int:factory_id>/delete/', delete_factory, name='delete_factory'),

]
