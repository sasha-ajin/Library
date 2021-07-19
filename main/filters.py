import django_filters
from django_filters import NumberFilter, DateFilter, ChoiceFilter,ModelChoiceFilter

from .models import Product, Order


class ProductFilter(django_filters.FilterSet):
    price__gt = NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['image', 'description', 'date_created', 'price']


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gt')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_created']

