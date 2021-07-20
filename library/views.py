from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LoginUserForm, CreateUserForm, DateTimeForm
from .models import time


# @login_required(login_url='log_in')
def main(request):
    form = DateTimeForm()
    context = {'form': form}
    return render(request, 'library/main.html',context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return redirect('log_in')

    context = {'form': form}
    return render(request, 'library/register.html', context)


def log_in(request):
    context = {}
    form = LoginUserForm()
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                return render(request, 'library/login.html')
    context['form'] = form
    return render(request, 'library/login.html', context)


@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('log_in')
