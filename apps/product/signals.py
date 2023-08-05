from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from .models import Category, Product, Price


@receiver(post_init, sender=Product)
def check_available(sender, instance, **kwargs):
    instance.available = False
    prices = Price.objects.filter(product=instance.id).order_by('-initial_balance', 'sold')
    if not prices:
        instance.available = False
    
    else:
        for price in prices:
            if price.stock_count() > 0:
                instance.available = True
                instance.save()

    for category in Category.objects.all():
        product_counts = Product.objects.filter(category=category).count()
        category.products_count = product_counts
        category.save()
