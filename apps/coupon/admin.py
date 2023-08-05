from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'percent', 'valid_to', 'apply_to', 'status')
    search_fields = ('title', 'code', 'percent')
    list_filter = ('status', 'valid_to')
    raw_id_fields = ('products', 'categories',)
