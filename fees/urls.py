from django.urls import path
from . import views



urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.addfees, name='addfees'),
    path('recorded/', views.recorded, name='recorded'),
    path('agreement/', views.agreement, name='agreement'),
]
