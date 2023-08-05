from django.template import Library
from apps.product.models import Price

register = Library()

@register.filter_function
def lower_price(queryset, args):
    args = [x.strip() for x in args.split(',')]
    prices = Price.objects.filter(product=queryset.id).order_by(*args)
    for item in prices:
        if item:
            if item.stock_count != 0:
                return item
    return False