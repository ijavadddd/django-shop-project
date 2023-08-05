from django.apps import AppConfig
from django_summernote.apps import DjangoSummernoteConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.main'
    verbose_name = 'خانه'


class TranslateDjangoSummernoteConfig(DjangoSummernoteConfig):
    verbose_name = 'آپلود'
    icon = 'fa-regular fa-pen-field'