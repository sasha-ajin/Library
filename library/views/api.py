from ..utils import date_to_json_string
from django.core import exceptions
import datetime
from ..models import Book, Order, TimeUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from ..serializers import OrderSerializer, BookSerializer


class OrderViewSet(ViewSet):
    def list(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        book = request.data['book']
        user = request.user.id
        start_date = request.time
        end_date = request.time + datetime.timedelta(days=int(request.data['days_to_rent']))
        # "2021-06-22T19:59:00Z"
        start_date = date_to_json_string(start_date)
        end_date = date_to_json_string(end_date)
        order = OrderSerializer(data={'start_date': start_date, 'end_date': end_date, 'user': user, 'book': book})
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
