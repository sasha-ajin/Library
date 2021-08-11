from .models import Time, Order, TimeUser
from datetime import datetime


class ChangingTimeForNowMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.time = TimeUser.objects.get(user=request.user).time
        else:
            request.time = datetime.now()
        response = self._get_response(request)
        return response
