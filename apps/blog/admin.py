from django.contrib import admin
from .models import Post
from django.db import models
from django.forms import TextInput, Textarea
from django_summernote.admin import SummernoteModelAdmin
from django_jalali.admin.filters import JDateFieldListFilter


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'author', 'publish_date', 'is_active')
    list_filter = ('author', ('publish_date', JDateFieldListFilter),)
    raw_id_fields = ('author',)
    search_fields = ('title',)
    prepopulated_fields = {'url': ('title',)}
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'style': 'width:min(100%, 700px)'})},
        models.TextField: {'widget': Textarea(attrs={'rows': '3'})}
    }
    autocomplete_fields = ('author',)


