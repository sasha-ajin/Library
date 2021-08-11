from django.db import models
from django.contrib.auth.models import User
from functools import reduce
from django.core import exceptions
import datetime


class Time(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.time.year}-{self.time.month}-{self.time.day} {self.time.hour}:{self.time.minute}"


class TimeUser(models.Model):
    time = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.time.year}-{self.time.month}-{self.time.day} {self.time.hour}:{self.time.minute} / {self.user}"


class Book(models.Model):
    COVERS = (
        ('Soft', 'Soft'),
        ('Hard', 'Hard'),
    )
    title = models.CharField(max_length=50, null=True)
    quantity_of_books = models.IntegerField()
    author = models.CharField(max_length=50, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=1000, null=False)
    cover = models.CharField(max_length=200, null=True, choices=COVERS)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def max_date_to_order(self, request):
        time_now = request.time
        max_available_date_to_order = time_now + datetime.timedelta(days=7)
        print(time_now)
        total_quantity_of_book = self.quantity_of_books
        orders_in_max_period = Order.objects.filter(start_date__lt=max_available_date_to_order,
                                                    end_date__gt=time_now, book=self).order_by('start_date')

        critical_points = list(orders_in_max_period.filter(start_date__gte=time_now).values_list(
            'start_date'))  # dates when quantity of ordered books changed

        critical_points += list(orders_in_max_period.filter(end_date__lt=max_available_date_to_order).values_list(
            'end_date'))
        critical_points.append([max_available_date_to_order])

        critical_points = sorted(reduce(lambda l1, l2: l1.extend(l2) or l1, critical_points, []))
        orders_in_max_period = Order.objects.filter(start_date__lt=max_available_date_to_order,
                                                    end_date__gt=time_now, book=self).order_by('start_date')
        print(orders_in_max_period)
        print(critical_points)
        max_endpoint = time_now
        for critical_point in critical_points:
            start_dates_before_critical_point = orders_in_max_period.filter(start_date__lt=critical_point).values_list(
                'start_date')
            end_dates_before_critical_point = orders_in_max_period.filter(end_date__lt=critical_point).values_list(
                'end_date')
            print(critical_point)
            print(start_dates_before_critical_point.count())
            ordered_books = start_dates_before_critical_point.count() - end_dates_before_critical_point.count()
            print(end_dates_before_critical_point.count())
            if ordered_books < total_quantity_of_book and critical_point >= max_endpoint:
                max_endpoint = critical_point
            else:
                return max_endpoint
        return max_endpoint

    def max_days_to_order(self, request):
        return (self.max_date_to_order(request=request) - request.time).days

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='orders')

    def __str__(self):
        return f" book {self.book} for {self.user}" \
               f" from {self.start_date.year}-{self.start_date.month}-{self.start_date.day} {self.start_date.hour}:{self.start_date.minute}" \
               f" to {self.end_date.year}-{self.end_date.month}-{self.end_date.day} {self.end_date.hour}:{self.end_date.minute} "

    def clean(self):
        if self.start_date > self.end_date:
            raise exceptions.ValidationError(f'start_date {self.start_date} is grater than end_date {self.end_date}')

    @property
    def rent_time(self):
        return self.end_date - self.start_date

    def time_to_return(self, request):
        return self.end_date - request.time
