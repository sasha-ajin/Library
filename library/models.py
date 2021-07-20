from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

time = models.DateTimeField()


class Time(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.time)

# class SiteUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=50, null=True)
#     email = models.EmailField(max_length=50, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class BookInCirculation(models.Model):
#     COVERS = (
#         ('Soft', 'Soft'),
#         ('Hard', 'Hard'),
#     )
#     title = models.CharField(max_length=50, null=True)
#     author = models.CharField(max_length=50, null=True)
#     page_quantity = models.BigIntegerField(null=False)
#     price = models.DecimalField(decimal_places=2, max_digits=1000, null=False)
#     cover = models.CharField(max_length=200, null=True, choices=COVERS)
#     image = models.ImageField(null=True, blank=True)
#
#     def __str__(self):
#         return self.title
#
#     @property
#     def free(self):
#         quantity_of_free_books = BookObject.objects.filter(book=self, free=True).count()
#         if quantity_of_free_books >= 1:
#             return True
#         else:
#             return False
#
#     @property
#     def image_url(self):
#         try:
#             url = self.image.url
#         except:
#             url = ''
#         return url
#
#
# class BookObject(models.Model):
#     book = models.ForeignKey(BookInCirculation, on_delete=models.CASCADE, null=False)
#     free = models.BooleanField()
#     customer = models.OneToOneField(SiteUser, on_delete=models.CASCADE, null=True, blank=True)
#     start_rent = models.DateTimeField(null=True)
#     end_rent = models.DateTimeField(null=True)
#
#     def __str__(self):
#         return f"{self.book.title} / Free: {self.free}"
