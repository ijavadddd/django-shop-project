from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.blog'
    verbose_name = 'بلاگ'
    icon = 'fa fa-book'