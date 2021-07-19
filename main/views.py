from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .util import create, update, delete
from .filters import ProductFilter, OrderFilter
from .models import Product, Order, Customer
from .forms import CustomerForm, ProductForm, OrderForm


def main_view(request):
    orders_total = Order.objects.count()
    order_pending = Order.objects.filter(status='Pending').count()
    order_delivered = Order.objects.filter(status='Delivered').count()
    products = Product.objects.all()
    orders = Order.objects.all()
    customers = Customer.objects.all()
    products_filter = ProductFilter(request.GET, queryset=products)
    products = products_filter.qs
    orders_filter = OrderFilter(request.GET, queryset=orders)
    orders = orders_filter.qs

    return render(template_name='main_page/main.html', request=request,
                  context={'products': products, 'orders': orders, 'customers': customers,
                           'orders_total': orders_total, 'order_pending': order_pending,
                           'order_delivered': order_delivered, 'orders_filter': orders_filter,
                           'products_filter': products_filter, })


class CustomerView(DetailView):
    model = Customer
    template_name = 'customer.html'
    context_object_name = 'customer'

    def get_object(self, queryset=None):
        pk_ = self.kwargs.get('pk')
        customer = get_object_or_404(Customer, pk=pk_)
        return customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ = self.kwargs.get('pk')
        customer_ = get_object_or_404(Customer, pk=pk_)
        context['orders'] = Order.objects.filter(customer=customer_)
        context['order_count'] = Order.objects.filter(customer=customer_).count()
        return context


def customer_create(request):
    return create(request=request, form_class=CustomerForm)


def customer_update(request, pk):
    return update(request=request, pk=pk, form_class=CustomerForm, object_class=Customer)


def customer_delete(request, pk):
    return delete(request=request, pk=pk, object_class=Customer)


def product_create(request):
    return create(request=request, form_class=ProductForm)


def product_update(request, pk):
    return update(request=request, pk=pk, form_class=ProductForm, object_class=Product)


def product_delete(request, pk):
    return delete(request=request, pk=pk, object_class=Product)


def order_create(request):
    return create(request=request, form_class=OrderForm)


def order_update(request, pk):
    return update(request=request, pk=pk, form_class=OrderForm, object_class=Order)


def order_delete(request, pk):
    return delete(request=request, pk=pk, object_class=Order)