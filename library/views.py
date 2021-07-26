import json
from .utils import date_to_json_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import views
from django.views.generic import FormView
from django.core import exceptions
import datetime

from .forms import LoginUserForm, CreateUserForm, DateTimeForm
from .models import Time, Book, Order

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ViewSet
from .serializers import OrderSerializer, BookSerializer


class Main(FormView):
    template_name = 'library/main.html'
    form_class = DateTimeForm

    def form_valid(self, form):
        time = form.cleaned_data['time']
        object_time = Time.objects.get(id=1)
        if object_time.time > time:
            print('Time was reduced')
        elif object_time.time < time:
            print('Time was increased')
        else:
            print('Time was not changed')
        object_time.time = time
        object_time.save()
        return redirect('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_time = Time.objects.get(id=1)
        context['time'] = object_time
        books = Book.objects.all()
        context['books'] = books
        return context


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
def my_profile(request):
    user_obj = request.user
    user_orders = Order.objects.filter(user=user_obj)

    quantity_user_orders = user_orders.count()
    context = {'quantity_user_orders': quantity_user_orders, 'user_orders': user_orders}

    user_returned_orders = Order.objects.filter(user=user_obj, end_date__lt=Time.objects.get(id=1).time)
    context['user_returned_orders'] = user_returned_orders
    context['quantity_user_returned_orders'] = user_returned_orders.count()

    user_not_returned_orders = Order.objects.filter(user=user_obj, end_date__gte=Time.objects.get(id=1).time)
    context['user_not_returned_orders'] = user_not_returned_orders
    context['quantity_user_not_returned_orders'] = user_not_returned_orders.count()

    return render(request, 'library/my_profile.html', context)


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
        start_date = Time.objects.get(id=1).time
        end_date = Time.objects.get(id=1).time + datetime.timedelta(days=7)
        # "2021-06-22T19:59:00Z"
        request.data['start_date'] = date_to_json_string(start_date)
        request.data['end_date'] = date_to_json_string(end_date)
        order = OrderSerializer(data=request.data)
        if not Book.objects.get(id=request.data['book']).free:
            return Response((['Book is not free']))
        if order.is_valid():
            order.save()
        return Response(order.data)

    def retrieve(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


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
