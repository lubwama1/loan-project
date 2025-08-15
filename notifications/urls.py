
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('notifications/', views.show_notifications, name='show-notifications'),

]
