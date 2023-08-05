from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from ..product.cart import Cart
from apps.product.models import Product, Price
from apps.product.forms import AddToCartForm


class AddToCartView(View):
    form_class = AddToCartForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def get(self,request):
        cart = Cart(request)
        return redirect(self.next)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            product = Product.objects.get(id=kwargs['product_id'])
            price = Price.objects.get(id=kwargs['price_id'])
            cart = Cart(request)
            cart.add(product, price, form.cleaned_data['quantity'])
            if self.next:
                messages.success(request, f'{product.title}&nbsp;به سبد خرید اضافه شد', 'success')
                return redirect(self.next)
            return redirect('dashboard:dashboard')
        messages.warning(request, 'مشکلی در افزودن به سبد خرید رخ داد، دوباره تلاش کنید', 'warning')
        return redirect('dashboard:dashboard')
