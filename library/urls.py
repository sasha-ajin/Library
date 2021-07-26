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

    path('api/order/', views.OrderViewSet.as_view({'get': 'list'}), name='rest_order_list'),
    path('api/order/<int:pk>/', views.OrderViewSet.as_view({'get': 'retrieve'}), name='rest_order_detail'),
    path('api/order/create/', views.OrderViewSet.as_view({'post': 'create'}), name='rest_order_create'),

    path('api/book/', views.BookView.as_view(), name='rest_book_list'),
    path('api/book/<int:pk>', views.BookDetailView.as_view(), name='rest_book_detail')
]
