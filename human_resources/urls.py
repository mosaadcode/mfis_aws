from django.urls import path
from . import views


urlpatterns = [

    path('', views.home, name='home2'),
    path('salary/', views.salary, name='salary'),
    path('perm/', views.perm, name='perm'),
    path('vacation/', views.vacation, name='vacation'),
    path('contact/', views.employee_contact, name='employee_contact'),

]