from django.contrib import admin
from .models import Slider, Brand


@admin.action(description="فعال سازی موارد انتخاب شده")
def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description="غیرفعال سازی موارد انتخاب شده")
def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('mini_img_preview', 'title', 'message', 'is_active')
    list_display_links = ('mini_img_preview', 'title', 'message')
    actions = (activate, deactivate)
    list_editable = ('is_active',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('mini_img_preview', 'title', 'is_active')
    list_display_links = ('mini_img_preview', 'title',)
    actions = (activate, deactivate)
    list_editable = ('is_active',)
