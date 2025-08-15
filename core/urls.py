
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('mark-as-read/', views.mark_notifications_as_read,
         name='mark_notifications_as_read'),
    path('contact/', views.contact, name='contact'),
]
