from django.urls import path
from . import views



urlpatterns = [
path('', views.fis_loginuser, name='fis_home'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('add/', views.addfees, name='addfees'),
    # path('recorded/', views.recorded, name='recorded'),
    # path('agreement/', views.agreement, name='agreement'),
    # #'''''''''''''''''''''
    # path('get_payment_methods/', views.get_payment_methods, name='get_payment_methods'),
    # path('execute_payment/', views.execute_payment, name='execute_payment'),
    # path('get_invoice_data/<int:invoice_id>/', views.get_invoice_data, name='get_invoice_data'),
]