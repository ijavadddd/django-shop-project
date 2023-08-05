from django.db import models
from django.urls import reverse
from django.conf import settings
from apps.product.models import Product, Price
import random


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE, verbose_name='کاربر')
    order_id = models.CharField(max_length=8, default=random.randint(10000000, 99999999), unique=True, verbose_name='شماره سفارش')
    created_at = models.DateTimeField(auto_created=True, verbose_name='سفارش داده شده در تاریخ')
    STATUS_LIST = [
        ('در حال پردازش', 'در حال پردازش'),
        ('ارسال شده', 'ارسال شده'),
        ('تحویل مرسوله به مشتری', 'تحویل مرسوله به مشتری'),
        ('لغو شده', 'لغو شده'),
        ('مرجوع شده', 'مرجوع شده'),
    ]
    tracking_code = models.CharField(max_length=30, null=True, blank=True, verbose_name='کد رهگیری پستی')
    receiver_name = models.CharField(max_length=100, verbose_name='نام گیرنده')
    receiver_phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن گیرنده')
    receiver_state = models.CharField(max_length=15, verbose_name='استان گیرنده')
    receiver_city = models.CharField(max_length=15, verbose_name='شهر گیرنده')
    receiver_address = models.CharField(max_length=650, verbose_name='آدرس گیرنده')
    receiver_postal_code = models.CharField(max_length=18, verbose_name='کدپستی  گیرنده')
    receiver_extra_data = models.CharField(max_length=350, blank=True, null=True, verbose_name='توضیحات اضافه')
    post_price = models.IntegerField(blank=True, null=True, verbose_name='هزینه پست')
    pay_method = models.CharField(max_length=15, default='online', blank=True, null=True, verbose_name='روش پرداخت')
    PAY_STATUS = [
        ('N', 'در انتظار پرداخت'),
        ('Y', 'پرداخت شده'),
    ]
    pay_status = models.CharField(max_length=35, choices=PAY_STATUS, default=PAY_STATUS[0], verbose_name='وضعیت پرداخت')
    status = models.CharField(max_length=40, choices=STATUS_LIST, default=STATUS_LIST[0][0], verbose_name='وضعیت')

    def total_price(self):
        count = 0
        for product in self.order_items.all():
            count += product.price.price * product.quantity
        return str(count)

    def __str__(self):
        return f'{self.order_id} - {self.status} - {self.created_at}'

    def get_absolute_url(self):
        return reverse('dashboard:order', args=(self.id,))

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    price = models.ForeignKey(Price, on_delete=models.SET_NULL, null=True, verbose_name='قیمت')
    quantity = models.IntegerField(null=True, default=1, verbose_name='تعداد')
    filled_price = models.CharField(max_length=12, blank=True, null=True, verbose_name='قیمت خریداری شده')
    discount = models.CharField(max_length=500, blank=True, null=True, verbose_name='میزان تخفیف')

    def get_absolute_url(self):
        return reverse('product:details', args=(self.product.id, self.product.slug))

    def __str__(self):
        return f'{self.product.title} - {self.filled_price}'

    class Meta:
        verbose_name = 'محصول سفارش داده شده'
        verbose_name_plural = 'محصولات سفارش داده شده'


class ReturnOrder(models.Model):
    return_order_id = models.CharField(max_length=8, default=random.randint(10000000, 99999999), unique=True,
                                       verbose_name='شماره سفارش مرجوعی')
    products = models.ManyToManyField(OrderProduct, related_name='returned_items', verbose_name='محصول')
    order = models.ForeignKey(Order, related_name='returns', on_delete=models.SET_NULL, null=True, verbose_name='سفارش')
    description = models.CharField(max_length=555, blank=True, null=True, verbose_name='توضیح')
    created_at = models.DateTimeField(auto_created=True, verbose_name='ساخته شده در')

    def total_price(self):
        count = 0
        for product in self.products.all():
            count += product.price.price * product.quantity
        return str(count)

    def get_absolute_url(self):
        return reverse('dashboard:returned_order', args=(self.return_order_id,))

    def __iter__(self):
        for item in self.__dict__:
            yield item

    def __str__(self):
        return f'{self.return_order_id} - {self.created_at}'

    class Meta:
        verbose_name = 'سفارش مرجوعی'
        verbose_name_plural = 'سفارشات مرجوعی'
