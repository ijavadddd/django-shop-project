from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.accounts'
    icon = 'fa fa-user'

    verbose_name = 'حساب کاربری'