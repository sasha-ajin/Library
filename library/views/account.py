from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django import views
from django.views.generic import FormView
from ..forms import LoginUserForm, CreateUserForm


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
