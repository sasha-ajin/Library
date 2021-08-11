from django import template

register = template.Library()


@register.simple_tag
def quantity_of_free_books(book, request_):
    return book.quantity_of_free(request=request_)


@register.simple_tag
def max_date_to_order(book, request_):
    return book.max_date_to_order(request=request_)


@register.simple_tag
def max_days_to_order(book, request_):
    return book.max_days_to_order(request=request_)


@register.simple_tag
def time_to_return(order, request_):
    return order.time_to_return(request=request_)


@register.filter(name='times')
def times(number):
    return range(1, number + 1)
