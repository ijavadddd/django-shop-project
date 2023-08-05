from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.product.models import Product, Category
from .models import Slider, Brand
from django.db.models import Q 


class HomeView(View):
    template_name = 'main/index.html'
    
    def get(self, request):
        return render(request, self.template_name, {})


class ProductSpecialOffersPartial(View):
    template_name = 'includes/product_slider.html'

    def get(self, request):
        products = Product.objects.order_by('-prices__special_offer')[:30]
        return render(request, self.template_name, {'products': products, 'slider_titile': 'محصولات ویژه', 'type': 'special_offer',})


class BestSellersProductPartial(View):
    template_name = 'includes/product_best_sellers.html'

    def get(self, request):
        old_product = Product.objects.order_by('-available','-prices__sold')[:1]
        products = Product.objects.order_by('-available', '-prices__sold',)[:6]
        return render(request, self.template_name, {'old_product': old_product, 'products': products, 
                                                    'slider_titile': 'پرفروش‌ترین‌ها',
                                                     'type': 'special_offer',})

class PopularCategories(View):
    template_name = "includes/popular_categories.html"
    
    def get(self, request):
        categories = Category.objects.order_by('-products_count',)[:6]
        return render(request, self.template_name, {'categories': categories})


class NewestProductsPartial(View):
    template_name = 'includes/product_slider.html'

    def get(self, request):
        products = Product.objects.order_by('-publish_date', '-update_date')[:10]
        return render(request, self.template_name, {'products': products, 'slider_titile': 'محصولات جدید', 'type': 'new',})


class SliderPartialView(View):
    def get(self, request):
        sliders = Slider.objects.filter(is_active=True)
        return render(request, 'main/slider_partial.html', {'sliders': sliders})


class BrandPartialView(View):
    def get(self, request):
        brands = Brand.objects.filter(is_active=True)
        return render(request, 'main/brand_partial.html', {'brands': brands})
