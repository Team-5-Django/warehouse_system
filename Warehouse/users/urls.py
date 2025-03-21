from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view , name='logout'),

    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete_account/', delete_account, name='delete_account'),

    path('adduser/', add_user , name='adduser'),
    path('approve-users/', approve_users, name='approve_users'),
    path('approve-user/<int:user_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:user_id>/', reject_user, name='reject_user'),
    
    path("edit-user/<int:user_id>/", edit_user, name="edit_user"),
    path("delete-user/<int:user_id>/", delete_user, name="delete_user"),

]
