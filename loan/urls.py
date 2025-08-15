
from django.urls import path
from . import views

app_name = 'loan'

urlpatterns = [
    path('loan-detail/<slug>/', views.loan_detail, name='loan-detail'),
    path('loan-application/<slug>/',
         views.loan_application_form, name='loan-application'),
    path('loan-types/', views.loan_list, name='loan-list'),
    path('loan-status/', views.loan_status, name='loan-status'),
    path('add-loan-product/', views.add_loan_product, name='add-loan'),
    path('my-applications/', views.my_applications, name='my-applications'),
    path('view-application/<int:pk>/',
         views.view_application, name='view-application'),
]
