from .utils import date_to_json_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django import views
from django.views.generic import FormView
from django.core import exceptions
import datetime
import operator

from .forms import LoginUserForm, CreateUserForm, DateTimeForm
from .models import Book, Order, TimeUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import OrderSerializer, BookSerializer


class Main(views.View):
    def post(self, request):
        form = DateTimeForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form_time = form.cleaned_data['time']
            current_time = TimeUser.objects.get(user=self.request.user)
            current_time.time = form_time
            current_time.save()
            return redirect('main')
        else:
            messages.info(request, 'Not valid date')
            return self.get(request)

    def get(self, request):
        context = {}
        context['time'] = request.time
        context['books'] = Book.objects.all()
        context['user'] = request.user.id
        context['form'] = DateTimeForm
        return render(request, 'library/main.html', context)


class Register(FormView):
    template_name = 'library/register.html'
    form_class = CreateUserForm

    def form_valid(self, form):
        form.save()
        return redirect('log_in')


class LogIn(views.View):
    def post(self, request):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return redirect('log_in')

    def get(self, request):
        form = LoginUserForm()
        context = {'form': form}
        return render(request, 'library/login.html', context)


@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')


class OrderViewSet(ViewSet):
    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        request.data['user'] = request.user.id
        start_date = request.time
        end_date = request.time + datetime.timedelta(days=int(request.data['days_to_rent']))
        # "2021-06-22T19:59:00Z"
        request.data['start_date'] = date_to_json_string(start_date)
        request.data['end_date'] = date_to_json_string(end_date)
        order = OrderSerializer(data=request.data)
        book = Book.objects.get(id=request.data['book'])
        if end_date > book.max_date_to_order(request=request):
            raise exceptions.ValidationError(f'Book {order.book.title} is not free in {end_date}')
        if order.is_valid():
            order.save()
        return Response(order.data)

    def retrieve(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@login_required(login_url='log_in')
def my_profile(request):
    user_obj = request.user
    time = request.time

    user_not_returned_orders = Order.objects.filter(user=user_obj, start_date__lte=time, end_date__gt=time)
    user_returned_orders = Order.objects.filter(user=user_obj, start_date__lt=time, end_date__lt=time)
    reservations = Order.objects.filter(start_date__gt=time, user=user_obj)
    context = {'user_not_returned_orders': user_not_returned_orders, 'user_returned_orders': user_returned_orders,
               'reservations': reservations, 'quantity_user_not_returned_orders': user_not_returned_orders.count(),
               'quantity_user_returned_orders': user_returned_orders.count(),
               'quantity_reservations': reservations.count}

    return render(request, 'library/my_profile.html', context)


class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetailView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        serializer = BookSerializer(book, many=False)
        return Response(serializer.data)

# class Main(FormView):
#     template_name = 'library/main.html'
#     form_class = DateTimeForm
#
#     def form_valid(self, form):
#         if self.request.user.is_authenticated:
#             form_time = form.cleaned_data['time']
#             # if object_time > form_time:
#             #     print('Time was reduced')
#             # elif object_time < form_time:
#             #     print('Time was increased')
#             # else:
#             #     print('Time was not changed')
#             current_time = TimeUser.objects.get(user=self.request.user)
#             current_time.time = form_time
#             current_time.save()
#         return redirect('main')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         object_time = self.request.time
#         context['time'] = object_time
#         books = Book.objects.all()
#         context['books'] = books
#         user = self.request.user.id
#         context['user'] = user
#         return context
