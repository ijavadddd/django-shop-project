from django.urls import path
from .views import (HomeView,
                    ProductSpecialOffersPartial, 
                    BestSellersProductPartial, 
                    PopularCategories,
                    NewestProductsPartial,
                    SliderPartialView,
                    BrandPartialView)


app_name = 'main'
urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('special-offer-products/',ProductSpecialOffersPartial.as_view(), name='product_special_offer_partial'),
    path('best-sellers-products/',BestSellersProductPartial.as_view(), name='best_sellers_product_partial'),
    path('popular-categories/',PopularCategories.as_view(), name='popular_categories_partial'),
    path('newset-products/',NewestProductsPartial.as_view(), name='newset_product_partial'),
    path('slider-partial/', SliderPartialView.as_view(), name='slider_partial'),
    path('brand-partial/', BrandPartialView.as_view(), name='brand_partial'),
]