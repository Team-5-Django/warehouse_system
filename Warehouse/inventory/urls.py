from django.urls import path
from .views import *
urlpatterns=[
    path("products/",products,name='products'),
    path('products/<int:product_id>/', productdetails.as_view(), name="productdetails"),
    path('category/',CategoryListView.as_view(),name="categoryproducts"),
    path('category/<int:category_id>/', category_products, name='category_products'),
    path('addproduct/', ProductCreateView.as_view(), name='add_product'),
    path('addcategory/', CategoryCreateView.as_view(), name='add_category'),
    path('editproduct/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('deleteproduct/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('deletecategory/<int:pk>/', CategoryDeleteView.as_view(), name='delete_category'),
 
]
