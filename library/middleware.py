from .models import Time, Order
from datetime import datetime


class ChangingTimeForNowMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        time_obj = Time.objects.get(id=1)
        time_obj.time = datetime.now()
        time_obj.save()
        response = self._get_response(request)
        return response


class DeleteNewOrdersMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        orders_from_the_future = Order.objects.filter(start_date__gt=Time.objects.get(id=1).time)
        for order in orders_from_the_future:
            order.delete()
        response = self._get_response(request)
        return response
