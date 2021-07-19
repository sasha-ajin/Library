from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView

from .models import Product, Order, Customer
from .forms import CustomerForm


def create(request, form_class):
    form = form_class()
    context = {'form': form}
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'forms/update_create.html', context)


def update(request, pk, form_class, object_class):
    object_for_update = object_class.objects.get(pk=pk)
    form = form_class(instance=object_for_update)
    context = {'form': form}

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=object_for_update)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'forms/update_create.html', context)


def delete(request, pk, object_class):
    object_for_delete = object_class.objects.get(pk=pk)
    if request.method == 'POST':
        object_for_delete.delete()
        return redirect('/')
    context = {'item': object_for_delete}

    return render(request, 'forms/delete.html', context)
