from django.apps import AppConfig


class OrderConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.order'
    verbose_name = 'سفارش'
    icon = 'fa fa-shopping-basket'
