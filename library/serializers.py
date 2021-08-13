from rest_framework import serializers
from .models import Order, Book


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def validate(self, data):
        start_date = data['start_date']
        end_date = data['end_date']
        book = data['book']
        if start_date > end_date:
            raise serializers.ValidationError(f'start date is grater than end_date.start date : {start_date}'
                                              f'end date: {end_date}')
        elif end_date > book.max_date_to_order(time_now=start_date):
            raise serializers.ValidationError(f'Book {book} is not valid in {end_date}')
        else:
            return data


class BookSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"
