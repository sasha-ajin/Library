from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django import views

from ..forms import DateTimeForm
from ..models import Book, Order, TimeUser


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
        print(Order.objects.all())
        context = {}
        context['time'] = request.time
        context['books'] = Book.objects.all()
        context['user'] = request.user.id
        context['form'] = DateTimeForm
        return render(request, 'library/main.html', context)


@login_required(login_url='log_in')
def my_profile(request):
    user_obj = request.user
    time = request.time
    user_not_returned_orders = Order.objects.active(time_now=time, user=user_obj)
    user_returned_orders = Order.objects.passive(time_now=time, user=user_obj)
    reservations = Order.objects.reservations(time_now=time, user=user_obj)
    context = {'user_not_returned_orders': user_not_returned_orders, 'user_returned_orders': user_returned_orders,
               'reservations': reservations, 'quantity_user_not_returned_orders': user_not_returned_orders.count(),
               'quantity_user_returned_orders': user_returned_orders.count(),
               'quantity_reservations': reservations.count}
    return render(request, 'library/my_profile.html', context)
