
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('applications/', views.admin_dashboard, name='applicants'),
    path('view-application/<int:pk>/', views.view_application, name='view-application'),
]
