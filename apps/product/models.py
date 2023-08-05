from django.db import models
from django.utils.html import mark_safe, format_html
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from apps.chat.models import Comment
from django.contrib import admin


class Category(models.Model):
    title = models.CharField(max_length=70, verbose_name='عنوان')
    url = models.SlugField(
                        max_length=130, 
                        unique=True, verbose_name='آدرس صفحه', 
                        help_text='این فبلد بر روی سئو تاثیر گذار است، موارد مربوطه رعایت شود')
    cover_img = models.ImageField(
                        upload_to='categories/', 
                        null=True, blank=True,
                        verbose_name='تصویر کاور',
                        help_text='این عکس به عنوان کاور محصول استفاده میشود')
    parent = models.ForeignKey(
                        'self', null=True, blank=True, on_delete=models.SET_NULL, 
                        related_name='children', 
                        verbose_name='والد',
                        help_text='والد دسته بندی را مشخص کنید')
    products_count = models.PositiveIntegerField(default=0, verbose_name='تعداد محصولات')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:products_by_category', args=(self.url,))

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی‌ها'


class Attribute(models.Model):
    title = models.CharField(max_length=35, verbose_name='عنوان')
    filter_title = models.SlugField(max_length=45, verbose_name='عنوان فیلتر')
    categories = models.ManyToManyField(
                        Category,
                        related_name='attributes',
                        verbose_name='دسته بندی‌ها',
                        help_text='تعیین کنید فیلتر مربوط به کدام دسته بندی‌ها است')

    def __str__(self):
            return self.title

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی‌ها'


class AttributeValue(models.Model):
    value = models.CharField(max_length=35, verbose_name='مقدار')
    filter_value = models.SlugField(max_length=45, verbose_name='مقدار فیلتر')
    attribute = models.ForeignKey(
                                'Attribute', on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='values',
                                verbose_name='ویژگی‌',
                                help_text='این مقدار متعلق به کدام ویژگی است')

    def __str__(self):
            return self.value

    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی'


class ProductAttribute(models.Model):
    title = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name='نام')
    value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE, verbose_name='مقدار')
    product = models.ForeignKey(
                        'Product',
                        on_delete=models.CASCADE,
                        related_name='attributes',
                        verbose_name='محصولات',
                        help_text='محصولاتی که این ویژگی را دارند درج کنید',)
    
    def __str__(self):
        return f'{self.title}: {self.value}'

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی‌های محصولات'


class Image(models.Model):
    image = models.ImageField(
                        upload_to='products/', 
                        verbose_name='تصویر',
                        help_text='این عکس به عنوان کاور محصول استفاده میشود')
    product = models.ForeignKey(
                        'Product',
                        on_delete=models.CASCADE,
                        related_name='images',
                        verbose_name='محصول',
                        help_text='محصولی که تصویر به آن تعلق دارد را انتخاب کنید',)


    def mini_img_preview(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.image))

    mini_img_preview.short_description = 'کاور'
    mini_img_preview.allow_tags = True

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'


class Product(models.Model):
    title = models.CharField(max_length=130, verbose_name='عنوان')
    brand = models.CharField(max_length=130, null=True, blank=True, verbose_name='برند', help_text='این فیلد اختیاری است')
    url = models.SlugField(
                        max_length=300, 
                        unique=True, verbose_name='آدرس صفحه', 
                        help_text='این فیلد بر روی سئو تاثیر گذار است، موارد مربوطه رعایت شود')
    cover_img = models.ImageField(
                        upload_to='products/covers/', 
                        null=True, blank=True,
                        verbose_name='تصویر کاور',
                        help_text='این عکس به عنوان کاور محصول استفاده میشود')
    category = models.ForeignKey(
                        Category, on_delete=models.SET_NULL,
                        null=True, blank=True, related_name='products',
                        verbose_name='دسته بندی')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات', help_text='معرفی و توضیحات را در این قسمت بنویسید')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    update_date = models.DateTimeField(auto_now=True, verbose_name='زمان آخرین تغییر')
    available = models.BooleanField(default=True, verbose_name='موجود')
    is_active = models.BooleanField(default=True, verbose_name='فعال؟')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,related_name='favorites', verbose_name='علاقه‌مندی‌ها`')
    comments = GenericRelation(Comment)




    def mini_img_preview(self):
        return mark_safe('<img src="/media/%s" height="60" />' % (self.cover_img))

    @admin.display
    def img_preview(self):
        return mark_safe('<img src="/media/%s" style="max-width:200px!important" />' % (self.cover_img))

    img_preview.short_description = 'تصویر'
    mini_img_preview.short_description = 'تصویر'
    mini_img_preview.allow_tags = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:details', args=(self.id, self.url))


    
    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class Color(models.Model):
    title = models.CharField(max_length=20, verbose_name='نام رنگ', help_text='به عنوان مثال قرمز')
    rgb = models.CharField(max_length=6, verbose_name='کد رنگ', help_text='کد rgb رنگ مورد نظر')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ‌ها'
        

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices',verbose_name='محصول')
    color = models.ForeignKey(
                            Color, 
                            null=True, blank=True,
                            on_delete=models.SET_NULL,
                            verbose_name='رنگ')
    attribute = models.ForeignKey(
                            ProductAttribute, 
                            null=True, blank=True,
                            on_delete=models.SET_NULL,
                            verbose_name='ویژگی', help_text='ویژگی تاثیر گذار در قیمت را وارد کنید')
    warranty = models.CharField(
                            max_length=50, 
                            null=True, blank=True,
                            verbose_name='گارانتی', help_text='میتوانید این فیلد را خالی بگذارید')
    price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت')
    discount_percent = models.FloatField(default=0, null=True, blank=True, verbose_name='درصد تخفیف')
    initial_balance = models.PositiveIntegerField(
                                            default=0,
                                            verbose_name='موجودی اولیه انبار',)
    sold = models.PositiveIntegerField(default=0, verbose_name='تعداد فروخته شده')
    special_offer = models.BooleanField(default=False, verbose_name='تخفیف ویژه')

    def stock_count(self):
        total = self.initial_balance - self.sold
        return total

    def real_price(self):
        price = (self.discount_percent * self.price) / 100
        return price

    def mini_cover_img(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.product.cover_img))


    stock_count.short_description = 'موجودی باقی مانده'
    real_price.short_description = 'قیمت بعد از اعمال تخفیف'
    mini_cover_img.short_description = 'کاور'

    def __str__(self):
        return f'{self.product.title} - تعداد موجود {self.stock_count()}'

    class Meta:
        verbose_name = 'قیمت محصول'
        verbose_name_plural = 'قیمت‌های محصولات'


admin.site.empty_value_display = "---"