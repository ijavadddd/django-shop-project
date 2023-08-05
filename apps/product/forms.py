from django import forms
from apps.order.models import Order

class AddToCartForm(forms.Form):
    product_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'product-id'}))
    price_id = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'price-id'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-number__input form-control form-control-lg', 'id': 'product-quantity', 'min': '1', 'value': '1'}), label='تعداد')


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'order_id', 'created_at', 'tracking_code', 'post_price', 'pay_status', 'status')
        widgets = {
            'receiver_name': forms.TextInput(attrs={'class': 'form-control', 'id':'receiver-name-id', 'placeholder': 'نام و نام خانوادگی'},),
            'receiver_state': forms.TextInput(attrs={'class': 'form-control', 'id':'receiver-state-id', 'placeholder': 'استان'}, ),
            'receiver_city': forms.TextInput(attrs={'class': 'form-control', 'id':'receiver-city-id', 'placeholder': 'شهر'},),
            'receiver_phone_number': forms.TextInput(attrs={'class': 'form-control', 'id':'receiver-phone-number-id', 'placeholder': 'شماره تلفن'}),
            'receiver_address': forms.TextInput(attrs={'class': 'form-control', 'id':'receiver-address-id', 'placeholder': 'آدرس'},),
            'receiver_postal_code': forms.TextInput(attrs={'class': 'form-control', 'id':'receiver-postal-code-id', 'placeholder': 'کد پستی'},),
            'receiver_extra_data': forms.Textarea(attrs={'class': 'form-control w-100', 'rows': '4', 'id':'receiver-extra-data-id', 'placeholder': 'توضیحات'}),
            'pay_method': forms.HiddenInput(attrs={'class': 'form-control', 'id':'pay-method-id', 'placeholder': 'روش پرداخت'},),
        }
        labels = {
            'receiver_name':'نام و نام خانوادگی',
            'receiver_state': 'استان',
            'receiver_city': 'شهر',
            'receiver_phone_number': 'شماره تلفن',
            'receiver_address': 'آدرس',
            'receiver_postal_code': 'کد پستی',
            'receiver_extra_data': 'توضیحات سفارش (اختیاری)',
            'pay_method': 'روش پرداخت',
        }