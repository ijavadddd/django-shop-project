from .models import Category
from .cart import Cart


def categories(request):
    categories = Category.objects.all()
    cart = Cart(request)
    if len(cart) > 0 :
        cart_count = len(cart)
    else:
        cart_count = 0
    return {'navbar_categories': categories, 'cart_count': cart_count}
