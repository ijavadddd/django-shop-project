from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import datetime
from django.urls import reverse
from django.utils.html import mark_safe


class User(AbstractBaseUser, PermissionsMixin):
    profile_img = models.ImageField(null=True, blank=True, verbose_name='تصویر پروفایل')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    date_of_birth = models.DateField(verbose_name='تاریخ تولد', null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, verbose_name='ایمیل', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال', help_text='بعد از وارد کردن کد ارسالی فعال میشود')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین')   
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def age(self):
        age = datetime.date.today() - self.date_of_birth
        return age

    def is_staff(self):
        return self.is_admin

    def min_profile_img(self):
        return mark_safe('<img src="/media/%s" height="50" />' % (self.profile_img))
        
    min_profile_img.short_description = 'تصویر'
    age.short_description = 'سن'
    is_staff.short_description = 'اجازه ورود به پنل امین'
    

    def __str__(self):
        return f'{self.first_name} {self.last_name} - ادمین: {self.is_admin}'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
        

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='کاربر')
    receiver_name = models.CharField(max_length=60, verbose_name='نام دریافت کننده', null=True)
    receiver_phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن دریافت کننده', null=True)
    state = models.CharField(max_length=20, verbose_name='استان', null=True)
    city = models.CharField(max_length=20, verbose_name='شهر', null=True)
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی', null=True)
    address = models.TextField(max_length=455, verbose_name='آدرس', blank=True, null=True)

    def __str__(self):
        return self.city

    def __iter__(self):
        address = self.__dict__
        for item in address.items():
            yield item

    def get_absolute_url(self):
        return reverse('dashboard:edit_address', args=(self.id,))

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'


class OTPCode(models.Model):
    user = models.ForeignKey(User, related_name='otp_codes', on_delete=models.CASCADE, verbose_name='کاربر')
    code = models.CharField(max_length=6, verbose_name='کد')
    valid_to = models.DateTimeField(null=True, verbose_name='معتبر تا')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کدهای یکبار مصرف'
