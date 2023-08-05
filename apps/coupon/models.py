from django.db import models
from apps.product.models import Product, Category


class Coupon(models.Model):
    title = models.CharField(max_length=25, verbose_name='عنوان')
    code = models.CharField(max_length=10, unique=True, verbose_name='کد تخفیف')
    percent = models.PositiveIntegerField(verbose_name='درصد تخفیف')
    APPLY_TO_LIST = [
        ('all', 'همه'),
        ('products', 'دسته بندی خاص'),
        ('categories', 'محصولات خاص'),
    ]
    apply_to = models.CharField(max_length=10, choices=APPLY_TO_LIST, default='all', verbose_name='اعمال روی')
    products = models.ManyToManyField(Product, related_name='coupons', verbose_name='محصولات')
    categories = models.ManyToManyField(Category, related_name='coupons', verbose_name='دسته بندی ها')
    valid_from = models.DateTimeField(verbose_name='فعال از تاریخ')
    valid_to = models.DateTimeField(verbose_name='فعال تا تاریخ')
    status = models.BooleanField(default=True, verbose_name='وضعیت')

    def __str__(self):
        return f'{self.title}: {self.code}'

    class Meta:
        verbose_name = 'کوپن'
        verbose_name_plural = 'کوپن ها'
