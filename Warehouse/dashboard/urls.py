from django.urls import path 
from .views import get_dashboard_page

urlpatterns = [
    path('', get_dashboard_page, name='dashboard')
]
