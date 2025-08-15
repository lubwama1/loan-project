
from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('repayment-schedule/<int:pk>/', views.repayment_schedule,
         name='repayment-schedule'),
]
