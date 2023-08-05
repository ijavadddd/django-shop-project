from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name='کاربر')
    message = models.CharField(max_length=800, verbose_name='متن')
    reply_to = models.ForeignKey(
                                'self', on_delete=models.CASCADE,
                                null=True, blank=True,
                                related_name='replies',
                                verbose_name='پاسخ به',
                                help_text='در صورتی که کامنت پاسخ کامنت دیگری باشد این قسمت پر میشود')
    publish_date = models.DateTimeField(auto_created=True, verbose_name='زمان انتشار')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='مدل', help_text='کامنت مربوط به کدام مدل است')
    object_id = models.PositiveIntegerField(verbose_name='آیدی رکورد مدل')
    content_object = GenericForeignKey('content_type', 'object_id')
    approved = models.BooleanField(
                                default=False, verbose_name='تایید شده', 
                                help_text='در صورتی که کامنت تایید شده باشد، نشان داده خواهد شد')
    
    def __str__(self):
        return f'{self.content_type} - {self.id}'

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت‌ها'
