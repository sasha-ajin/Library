from django.urls import path
from .views import render, api, account

urlpatterns = [
    path('', render.Main.as_view(), name='main'),
    path('my_profile/', render.my_profile, name='my_profile'),

    path('register/', account.Register.as_view(), name='register'),
    path('log_in/', account.LogIn.as_view(), name='log_in'),
    path('log_out/', account.log_out, name='log_out'),

    path('api/order/', api.OrderViewSet.as_view({'get': 'list'}), name='rest_order_list'),
    path('api/order/<int:pk>/', api.OrderViewSet.as_view({'get': 'retrieve'}), name='rest_order_detail'),
    path('api/order/create/', api.OrderViewSet.as_view({'post': 'create'}), name='rest_order_create'),

    path('api/book/', api.BookView.as_view(), name='rest_book_list'),
    path('api/book/<int:pk>', api.BookDetailView.as_view(), name='rest_book_detail')
]
