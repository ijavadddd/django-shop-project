from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import AddToCartForm
from .models import Product, Category, Price
from django.core.paginator import Paginator
from django.http import HttpResponse
from apps.chat.models import Comment
from apps.chat.forms import CommentForm
from .forms import CheckoutForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .cart import Cart
from django.http import JsonResponse


class Details(View):
    template_name = 'product/details.html'
    form_class = AddToCartForm

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=kwargs.get('pk'))
        self.comments = self.product.comments.filter(approved=True).order_by('-publish_date')
        paginator = Paginator(self.comments, 10)
        page_number = request.GET.get('page')
        self.comments_objects = paginator.get_page(page_number)
        self.comment_form = CommentForm
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.product.is_active:
            return redirect('main:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.product.prices.exists():
            add_to_cart_form = self.form_class(request.POST or None, initial={'price_id': self.product.prices.all()[0].id,
            'product_id': self.product.id})

            return render(request, self.template_name, {'add_to_cart_form': add_to_cart_form, 'product': self.product,
                                                        'comments': self.comments_objects,
                                                        'comment_form': self.comment_form, 'comments_count': self.comments.count()})

        return render(request, self.template_name, {'product': self.product,
                                                    'comments': self.comments_objects,
                                                    'comment_form': self.comment_form,
                                                    'comments_count': self.comments.count()})

class CategoryView(View):
    template_name = 'product/categories.html'

    def get(self, request, *args, **kwargs):
        if kwargs['url'] != 'None':
            categories = Category.objects.filter(parent__url=kwargs['url'])
        else:
            categories = Category.objects.filter(parent=None)
        return render(request, self.template_name, {'categories': categories})


class ProductCategoryView(View):
    template_name = 'product/products.html'

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, url=kwargs['url'])
        products = Product.objects.filter(category=category).order_by('-available', '-publish_date')
        newest_related_product = Product.objects.filter(category=category).order_by('-available', '-publish_date')[:5]
        paginator = Paginator(products, 25)
        page_number = request.GET.get('page')
        products_objects = paginator.get_page(page_number)
        return render(request, self.template_name, {'category': category, 'products': products_objects, 'newest_related_product': newest_related_product})


class RelatedProductsPartial(View):
    template_name = 'includes/product_slider.html'

    def get(self, request, category_id):
        products = Product.objects.filter(category=category_id)[:25]
        return render(request, self.template_name, {'products': products})


class AddToFavorites(View):
    def get(self, request):
        user = request.user.id
        product = get_object_or_404(Product, id=request.GET['product_id'])
        product.likes.add(user)
        product.save()
        return HttpResponse("Success")


class RemoveFromFavorites(View):
    def get(self, request):
        user = request.user.id
        product = get_object_or_404(Product, id=request.GET['product_id'])
        product.likes.remove(user)
        product.save()
        return HttpResponse("Success")


class AddCommentView(View):
    form_class = CommentForm

    def post(self, request, product_id):
        form = self.form_class(request.POST)
        product_type = ContentType.objects.get(model='product')
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_comment = Comment.objects.create(
                message=cleaned_data['message'],
                user=request.user,
                content_type=product_type,
                object_id = product_id
            )
            if cleaned_data['reply_to'] != '0':
                reply_to_value = Comment.objects.get(id=cleaned_data['reply_to'])
                new_comment.reply_to = reply_to_value
                new_comment.save()
            return HttpResponse("Success")


class AddToCartView(View):
    form_class = AddToCartForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cart = Cart(request)
            cart.add(request, cleaned_data['product_id'], cleaned_data['price_id'], cleaned_data['quantity'])
            return JsonResponse({'cart_count': len(cart)})


class CartView(View):

    def get(self, request):
        cart = Cart(request)
        return render(request, 'product/cart.html', {'cart': cart})


class RemoveFromCartView(View):

    def post(self, request):
        cart = Cart(request)
        cart.remove(request, request.POST['product_id'], request.POST['price_id'])
        return HttpResponse('Success')


class CheckoutView(View):
    template_name = 'product/checkout.html'
    form_class = CheckoutForm

    def get(self, request):
        cart = Cart(request)
        return render(request, self.template_name, {'form_checkout': self.form_class, 'cart': cart})
