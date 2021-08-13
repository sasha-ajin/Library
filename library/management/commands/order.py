from library.models import Order, Book
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import datetime
import random
from django.utils.timezone import make_aware


class Command(BaseCommand):
    help = "Order generate"

    def add_arguments(self, parser):
        parser.add_argument(
            '-vi',
            '--view',
            type=str,
            default=False,
            help='Вывод короткого сообщения'
        )
        parser.add_argument(
            '-gn_rn_ord',
            '--generate_random_orders',
            nargs=3,
            # type=str,
            default=False,
            help='Вывод короткого сообщения'
        )

    def handle(self, *args, **options):
        if options['view']:
            index = options['view']
            if index == '.':
                for order in Order.objects.all():
                    self.stdout.write(str(order))
            else:
                try:
                    self.stdout.write(str(Order.objects.get(pk=int(index))))
                except Exception:
                    self.stdout.write(f"There's no order with pk {index}")

        elif options['generate_random_orders']:
            min_date = make_aware(datetime.datetime.strptime(options['generate_random_orders'][0], '%Y-%m-%d/%H:%M'))
            max_date = make_aware(datetime.datetime.strptime(options['generate_random_orders'][1], '%Y-%m-%d/%H:%M'))
            times = int(options['generate_random_orders'][2])
            if min_date < max_date:
                self.stdout.write(f"Creating {times} random orders between  {str(min_date)} and {max_date} ")
                for time in range(times):
                    book = random.choice(Book.objects.all())
                    user = random.choice(User.objects.all())
                    start_date = min_date + random.random() * (max_date - min_date)
                    end_date = start_date + random.random() * (max_date - start_date)
                    order = Order.objects.create(book=book, user=user, start_date=start_date, end_date=end_date)
                    order.save()
                    self.stdout.write(
                        self.style.SUCCESS(f"Order with {order} successfully created"))
            else:
                self.stdout.write(f"start date {min_date} is less or equal to max date {max_date} ")


"""
Questions:
1)If arguments are from different types
2)Is option view correct
"""