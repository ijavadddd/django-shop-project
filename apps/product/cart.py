from django.contrib import messages
from apps.product.models import Product, Price


# id of cart session
CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        # get cart session
        cart = self.session.get(CART_SESSION_ID)
        # if cart session not exists set cart variable
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __getitem__(self, item):
        return self.cart[item]

    def get(self, key):
        if key in self.cart.keys():
            return True

    def new_quantity(self, key, quantity):
        new_quantity = self.cart[key]['quantity'] + quantity
        return new_quantity

    def add(self, request, product_id, price_id, quantity):
        key = f'{product_id}_{price_id}'
        price = Price.objects.get(id=price_id)
        if self.cart.get(key):
            if self.new_quantity(key, quantity) <= price.stock_count():
                self.cart[f'{product_id}_{price_id}']['quantity'] += quantity
            else:
                self.cart[f'{product_id}_{price_id}']['quantity'] = price.stock_count()
            self.save()


        else:
            self.cart[f'{product_id}_{price_id}'] = {
                'product_id': product_id,
                'price_id': price_id,
                'quantity': quantity,
            }
            self.save()

    # remove product from cart
    def remove(self, request, product_id, price_id):
        key = f'{product_id}_{price_id}'
        if self.cart.get(key):
            del self.cart[key]
            self.save()

    # clear cart
    def clear(self):
        self.cart = None
        self.save()

    # total price of all products in cart
    def total_price(self):
        total = 0
        for item in self:
            total += item['total']
        return total

    def save(self):
        self.session.modified = True

    def __iter__(self):
        products_ids = self.cart.keys()
        cart = self.cart.copy()
        for product_id in products_ids:
            product = Product.objects.get(id=cart[f'{product_id}']['product_id'])
            price = Price.objects.get(id=cart[f'{product_id}']['price_id'])
            cart[f'{product.id}_{price.id}']['cover_img'] = product.cover_img
            cart[f'{product.id}_{price.id}']['title'] = product.title
            # cart[f'{product.id}_{price.id}']['warranty'] = price.warranty.title
            cart[f'{product.id}_{price.id}']['price'] = price.price
            if price.color:
                cart[f'{product.id}_{price.id}']['color'] = price.color
            else:
                cart[f'{product.id}_{price.id}']['attribute'] = price.attribute
            if price.price:
                cart[f'{product.id}_{price.id}']['total'] = cart[f'{product.id}_{price.id}']['price'] * cart[f'{product.id}_{price.id}']['quantity']
            else:
                cart[f'{product.id}_{price.id}']['total'] = '0'
            cart[f'{product.id}_{price.id}']['stock_count'] = price.stock_count()
            cart[f'{product.id}_{price.id}']['get_absolute_url'] = product.get_absolute_url()

        for product in cart.values():
            yield product

    # quantity of products in cart
    def __len__(self):
        if not self.cart:
            return 0
        return sum(int(product['quantity']) for product in self.cart.values())

    def empty(self):
        if self.cart:
            return False
        return True
