from django.db import models
import datetime
import random
from django.conf import settings
from tinymce.models import HTMLField
from django.urls import reverse


def image_directory(instance, filename):
    image_name = filename.split('.')[0]
    image_suffix = filename.split('.')[-1]
    this_moment = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d_%H:%M:%s:%f")
    random_number = random.randint(1000000, 9999999)
    final_dire = f'static/images/blog/{image_name}_{this_moment}_{random_number}.{image_suffix}'
    return final_dire


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.SET_NULL, null=True, verbose_name='نویسنده')
    cover_img = models.ImageField(upload_to=image_directory, blank=True, null=True, verbose_name='عکس اصلی')
    title = models.CharField(max_length=185, verbose_name='عنوان')
    url = models.SlugField(max_length=220, unique=True, verbose_name='آدرس صفحه')
    content = HTMLField(verbose_name='محتوا')
    short_description = models.TextField(max_length=500, blank=True, null=True, verbose_name='توضیح کوتاه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    publish_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')

    def get_absolute_url(self):
        return reverse('blog:post', args=(self.id, self.url))

    def __str__(self):
        return f'{self.title} - {self.author.first_name} {self.author.last_name} - {self.publish_date}'

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

