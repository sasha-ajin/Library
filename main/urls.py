from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),

    path('customer_profile/<str:pk>/', views.CustomerView.as_view(), name='customer'),
    path('customer_create/', views.customer_create, name='customer_create'),
    path('customer_update/<str:pk>/', views.customer_update, name='customer_update'),
    path('customer_delete/<str:pk>/', views.customer_delete, name='customer_delete'),

    path('product_create/', views.product_create, name='product_create'),
    path('product_update/<str:pk>/', views.product_update, name='product_update'),
    path('product_delete/<str:pk>/', views.product_delete, name='product_delete'),

    path('order_create/', views.order_create, name='order_create'),
    path('order_update/<str:pk>/', views.order_update, name='order_update'),
    path('order_delete/<str:pk>/', views.order_delete, name='order_delete'),

]
