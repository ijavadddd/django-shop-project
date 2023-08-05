from django.db import models
from django.utils.html import mark_safe


class Slider(models.Model):
    img = models.ImageField(upload_to='files/', verbose_name='عکس اسلایدر')
    title = models.CharField(max_length=130, null=True, blank=True, verbose_name='عنوان')
    message = models.CharField(max_length=500, verbose_name='توضیحات', null=True, blank=True,)
    button_action = models.CharField(
                    max_length=300, 
                    null=True, blank=True,
                    verbose_name='لینک دکمه', help_text='یا لینکم ستقسم خارجی یا به صورت ‌{% "urls "Address %}')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def mini_img_preview(self):
        return mark_safe('<img src="/media/%s" style="max-height:50px!important" />' % (self.img))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدرها'

    mini_img_preview.short_description = 'تصویر'


class Brand(models.Model):
    img = models.ImageField(upload_to='files/', verbose_name='عکس اسلایدر')
    title = models.CharField(max_length=20, null=True, blank=True ,verbose_name='عنوان',
                             help_text='برای سيوی بهتر این فیلد را پر کنید')
    is_active = models.BooleanField(default=True, verbose_name='قعال')

    def mini_img_preview(self):
        return mark_safe('<img src="/media/%s" style="max-height:50px!important" />' % (self.img))

    def __str__(self):
        return self.img.url

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'

    mini_img_preview.short_description = 'تصویر'
