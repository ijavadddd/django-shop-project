from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'apps.chat'
    verbose_name = 'چت'
    icon = 'fa-solid fa-messages'
