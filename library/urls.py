from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    path('register/', views.register, name='register'),
    path('log_in/', views.log_in, name='log_in'),
    path('log_out/', views.log_out, name='log_out')
]
