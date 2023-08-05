from django.contrib import admin
from .models import OrderProduct, Order, ReturnOrder
from .forms import OrderForm, ReturnOrderForm


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    search_fields = ('product',)
    autocomplete_fields = ('product',)

    fieldsets = [
        (
            None,
            {'fields':
                (
                    'order',
                    ('product', 'price'),
                    ('filled_price', 'discount'),
                    'quantity'

                )
            }
        )
    ]


class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    search_fields = ('product',)
    autocomplete_fields = ('product', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('order_id', 'tracking_code', 'status', 'created_at')
    search_fields = ('tracking_code',)
    list_filter = ('status',)
    inlines = (OrderProductInline,)

    fieldsets = [
        (
            None,
            {'fields': (
                'user',
                ('order_id', 'tracking_code'),
                ('receiver_name', 'receiver_phone_number'),
                ('receiver_state', 'receiver_city'),
                ('receiver_postal_code', 'receiver_address',),
                'receiver_extra_data',
                ('pay_method', 'pay_status'),
                'post_price',
                'status',
                'created_at'
            )}
        )
    ]


@admin.register(ReturnOrder)
class ReturnOrderAdmin(admin.ModelAdmin):
    form = ReturnOrderForm
    list_display = ('return_order_id', 'order', 'created_at')
    search_fields = ('return_order_id', 'order')
    filter_horizontal = ('products',)
    fieldsets = [
        (
            None,
            {'fields':
                (
                    ('order', 'return_order_id'),
                    'description',
                    'products',
                    'created_at'
                )}
        )
    ]
