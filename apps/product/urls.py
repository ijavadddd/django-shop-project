from django.urls import path
from .views import (Details, 
    CategoryView, 
    ProductCategoryView,
    RelatedProductsPartial, 
    AddToFavorites,
    RemoveFromFavorites,
    AddCommentView, 
    AddToCartView, 
    CartView,
    RemoveFromCartView,
    CheckoutView)


app_name = 'product'
urlpatterns = [
    path('<int:pk>/<slug:url>/', Details.as_view(), name='details'),
    path('category/<slug:url>/', CategoryView.as_view(), name='category'),
    path('in-category/<slug:url>/', ProductCategoryView.as_view(), name='products_by_category'),
    path('related-products/<int:category_id>/', RelatedProductsPartial.as_view(), name='related_products_partial'),
    path('add-to-favrites/', AddToFavorites.as_view(), name='add_to_favorites'),
    path('remove-from-favorites/', RemoveFromFavorites.as_view(), name='remove_from_favorites'),
    path('add-comment/<int:product_id>/', AddCommentView.as_view(), name='add_comment'),
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove_from_card'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
