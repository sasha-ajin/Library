from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Main.as_view(), name='main'),
    path('my_profile/', views.my_profile, name='my_profile'),
    # path('', views.main, name='main'),

    path('register/', views.Register.as_view(), name='register'),
    path('log_in/', views.LogIn.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),

    path('api/order/', views.OrderListView.as_view(), name='rest_order_list'),
    path('api/order/<int:pk>/', views.OrderDetailView.as_view(), name='rest_order_detail'),
    path('api/order/create/', views.OrderCreateView.as_view(), name='rest_order_create'),
]
