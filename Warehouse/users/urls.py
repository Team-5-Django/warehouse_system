from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view , name='logout'),
    path('adduser/', add_user , name='adduser'),
    path('dashboard/', dashboard, name='dashboard'),
]
