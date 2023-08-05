from django.apps import AppConfig
from django_summernote.apps import DjangoSummernoteConfig


class AdminSoftDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_soft'
    icon = 'fa fa-user'

class TranslateDjangoSummernoteConfig(DjangoSummernoteConfig):
    verbose_name = 'ویرایشگر متنی'