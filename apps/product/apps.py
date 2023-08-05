from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.product'
    verbose_name = 'محصول'
    icon = 'fa fa-shopping-bag'

    def ready(self):
        from .import signals