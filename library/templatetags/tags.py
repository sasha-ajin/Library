from django import template

register = template.Library()


@register.simple_tag
def quantity_of_free_books(book, time_now):
    return book.quantity_of_free(time_now=time_now)


@register.simple_tag
def max_date_to_order(book, time_now):
    return book.max_date_to_order(time_now=time_now)


@register.simple_tag
def max_days_to_order(book, time_now):
    return book.max_days_to_order(time_now=time_now)


@register.simple_tag
def time_to_return(order, time_now):
    return order.time_to_return(time_now=time_now)


@register.filter(name='times')
def times(number):
    return range(1, number + 1)
