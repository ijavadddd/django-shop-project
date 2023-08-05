from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from .models import Comment
from .forms import CommentAdminForm


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ('user', 'message', 'publish_date', 'approved')
    search_fields = ('user', 'message')
    list_filter = ('approved', 'content_type')

    fieldsets = [
        (
            None,
            {'fields':
                (
                    'approved',
                    'user',
                    'reply_to',
                    'message',
                    ('content_type', 'object_id'),
                    'publish_date',
                )}
        )
    ]
