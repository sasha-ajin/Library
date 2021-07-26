from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.core import exceptions


class Time(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str(self.time)
        return f"{self.time.year}-{self.time.month}-{self.time.day} {self.time.hour}:{self.time.minute}"


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

    @property
    def quantity_of_free(self):
        not_free_books = Order.objects.filter(book=self, end_date__gte=Time.objects.get(id=1).time)
        quantity_not_free_books = not_free_books.count()
        return self.quantity_of_books - quantity_not_free_books

    @property
    def free(self):
        not_free_books = Order.objects.filter(book=self, end_date__gte=Time.objects.get(id=1).time)
        quantity_not_free_books = not_free_books.count()
        quantity_of_free = self.quantity_of_books - quantity_not_free_books
        if quantity_of_free > 0:
            return True
        else:
            return False

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    start_date = models.DateTimeField(default=Time.objects.get(id=1).time)
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
        if not self.book.free:
            raise exceptions.ValidationError("Book is not free")

    def rent_time(self):
        return self.end_date - self.start_date

    def time_to_return(self):
        return self.end_date - Time.objects.get(id=1).time
