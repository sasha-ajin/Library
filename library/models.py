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
    price = models.DecimalField(decimal_places=2, max_digits=60, null=False)
    cover = models.CharField(max_length=200, null=True, choices=COVERS)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def max_date_to_order(self, time_now):
        max_available_date_to_order = time_now + datetime.timedelta(days=7)
        total_quantity_of_book = self.quantity_of_books
        orders_in_max_period = Order.objects.filter(start_date__lt=max_available_date_to_order,
                                                    end_date__gt=time_now, book=self).order_by('start_date')
        critical_points = [max_available_date_to_order]
        for order in orders_in_max_period:
            if order.start_date >= time_now:
                critical_points += [order.start_date]
            if order.end_date < max_available_date_to_order:
                critical_points += [order.end_date]
        critical_points = list(dict.fromkeys(critical_points))  # deleting duplicates
        critical_points.sort()
        max_endpoint = time_now
        for critical_point in critical_points:
            start_dates_before_critical_point = int()
            end_dates_before_critical_point = int()
            for order in orders_in_max_period:
                if order.start_date < critical_point:
                    start_dates_before_critical_point += 1
                if order.end_date < critical_point:
                    end_dates_before_critical_point += 1
            ordered_books = start_dates_before_critical_point - end_dates_before_critical_point
            if ordered_books < total_quantity_of_book and critical_point >= max_endpoint:
                max_endpoint = critical_point
            else:
                return max_endpoint
        return max_endpoint

    def max_days_to_order(self, time_now):
        return (self.max_date_to_order(time_now=time_now) - time_now).days

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderManager(models.Manager):
    def active(self, time_now, user):
        return super(OrderManager, self).get_queryset().filter(user=user, start_date__lte=time_now,
                                                               end_date__gt=time_now)

    def passive(self, time_now, user):
        return super(OrderManager, self).get_queryset().filter(user=user, start_date__lt=time_now,
                                                               end_date__lt=time_now)

    def reservations(self, time_now, user):
        return super(OrderManager, self).get_queryset().filter(start_date__gt=time_now, user=user)


class Order(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='orders')
    objects = OrderManager()

    def __str__(self):
        return f" book {self.book} for {self.user}" \
               f" from {self.start_date.year}-{self.start_date.month}-{self.start_date.day} {self.start_date.hour}:" \
               f"{self.start_date.minute} to {self.end_date.year}-{self.end_date.month}-{self.end_date.day} " \
               f"{self.end_date.hour}:{self.end_date.minute} "

    def clean(self):
        if self.start_date > self.end_date:
            raise exceptions.ValidationError(f'start_date {self.start_date} is grater than end_date {self.end_date}')
        elif self.end_date > self.book.max_date_to_order(time_now=self.start_date):
            raise exceptions.ValidationError(f'Book {self.book} is not valid in {self.end_date}')

    @property
    def rent_time(self):
        return self.end_date - self.start_date

    def time_to_return(self, time_now):
        return self.end_date - time_now
