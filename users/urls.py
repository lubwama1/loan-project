
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.userLogineView.as_view(), name='login'),
    path('signup/', views.register, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
]
