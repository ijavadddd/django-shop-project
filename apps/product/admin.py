from django.contrib import admin
from .models import (
    Product,
    Category,
    Attribute,
    AttributeValue,
    ProductAttribute,
    Image,
    Color,
    Price,
)
from django_summernote.admin import SummernoteModelAdmin
from admin_decorators import (short_description, limit_width, boolean,
                              apply_filter, order_field, allow_tags)
from django.db.models.aggregates import Count
# from django_admin_listfilter_dropdown.filters import DropdownFilter
from admin_searchable_dropdown.filters import AutocompleteFilter
from django.db import models
from django import forms
from more_admin_filters import MultiSelectDropdownFilter, DropdownFilter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'products_count')
    list_display = ('title', 'products_count')
    prepopulated_fields = {'url': ('title',), }
    raw_id_fields = ('parent',)
    search_fields = ('title',)
    list_filter = (('title', DropdownFilter),)


class AttributeValueInlineAdmin(admin.TabularInline):
    model = AttributeValue
    extra = 2


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = (
        ('categories__title', DropdownFilter),
    )
    search_fields = ('categories',)
    prepopulated_fields = {'filter_title': ('title',)}
    inlines = (AttributeValueInlineAdmin,)
    filter_vertical = ('categories',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('value',)
    prepopulated_fields = {'filter_value': ('value',)}
    raw_id_fields = ('attribute',)
    search_fields = ('value',)
    autocomplete_fields = ('attribute',)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('title', 'value',)
    raw_id_fields = ('title', 'value')
    search_fields = ('title', 'value')
    autocomplete_fields = ('title', 'value')

    fieldsets = [
        (
            None,
            {'fields':
                (
                    'title',
                    'value',
                )}
        )
    ]


class ProductAttributeInlineAdmin(admin.TabularInline):
    model = ProductAttribute
    extra = 0
    autocomplete_fields = ('title', 'value')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('mini_img_preview', 'image')


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('title', 'rgb')
    search_fields = ('title', 'rgb')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('mini_cover_img', 'price', 'color', 'stock_count', 'sold')
    raw_id_fields = ('product', 'color')
    readonly_fields = ('stock_count', 'real_price')
    search_fields = ('product',)
    autocomplete_fields = ('product', 'color', 'attribute')
    fieldsets = [
        (
            None,
            {'fields':
                (
                    'product',
                    'warranty',
                    ('color', 'attribute',),
                    ('initial_balance', 'sold', 'stock_count'),
                    ('price', 'discount_percent', 'real_price'),
                    'special_offer',
                )
            }
        ),
    ]


class PriceInlineAdmin(admin.StackedInline):
    model = Price
    list_display = ('mini_cover_img', 'price', 'color', 'stock_count', 'sold')
    readonly_fields = ('stock_count', 'real_price')
    autocomplete_fields = ('product', 'color', 'attribute')
    extra = 0
    fieldsets = [
        (
            None,
            {'fields':
                (
                    'warranty',
                    ('color', 'attribute',),
                    ('initial_balance', 'sold', 'stock_count'),
                    ('price', 'discount_percent', 'real_price'),
                    'special_offer',
                )
            }
        ),
    ]


class ImageAdminInline(admin.TabularInline):
    model = Image
    fk_name = 'product'
    extra = 0
    readonly_fields = ('mini_img_preview',)


class ProductCategoryFilter(AutocompleteFilter):
    title = 'دسته بندی'
    field_name = 'category'


@admin.action(description="غیرفعال سازی موارد انتخاب شده")
def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description="فعال سازی موارد انتخاب شده")
def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin, admin.ModelAdmin):
    actions_on_bottom = True
    list_filter = [ProductCategoryFilter,
                   'available'
                   ]
    empty_value_display = '---'
    summernote_fields = ('description',)
    list_display = (
        'mini_img_preview', 'title', 'category', 'publish_date', 'update_date', 'available', 'count_likes_number',
        'is_active')
    list_display_links = ('mini_img_preview', 'title',)
    actions = [activate, deactivate]
    prepopulated_fields = {'url': ('title', 'brand'), }
    ordering = ('-update_date', '-publish_date')
    readonly_fields = ('available', 'img_preview')
    inlines = (ImageAdminInline, ProductAttributeInlineAdmin, PriceInlineAdmin)
    list_editable = ('is_active',)
    list_per_page = 25
    list_select_related = ('category',)
    autocomplete_fields = ('category',)
    save_as = True
    save_on_top = True
    search_fields = ('title', 'brand', 'category__title')
    search_help_text = 'میتوانید عنوان، برند یا دسته بندی محصول را جستجو کنید'

    fieldsets = (
        (
            None,
            {
                'fields': [
                    'img_preview',
                    'cover_img',
                    ('title', 'brand'),
                    ('url', 'category'),
                ],
                'description': 'برای نتایج یهتر حتما تمامی فیلدهای این بخش را پر کنید'
            },
        ),
        (
            'بیشتر',
            {
                'fields': [
                    'description',
                    ('available', 'is_active')
                ],

            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(likes_count=Count('likes'))
        return qs

    @short_description('تعداد لایک')
    @order_field('likes_count')
    def count_likes_number(self, obj):
        return obj.likes_count
