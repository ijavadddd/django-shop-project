from cProfile import label

from django import forms
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from apps.accounts.models import User, Address
from apps.order.models import ReturnOrder, Order, OrderProduct


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'شماره تلفن خود را وارد کنید', 'readonly': ''}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خود را وارد کنید'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی خود را وارد کنید'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'placeholder': 'ایمیل شما'}),
        }


class PasswordChangeForm(BasePasswordChangeForm):
    error_messages = {
        'password_mismatch': ('رمز عبور جدید با تکرار آن مطابقت ندارد'),
        'password_incorrect': ("رمز عبور فعلی درست وارد نشده"),
    }
    old_password = forms.CharField(
        label='رمز عبور فعلی',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'autofocus': True,
                                          'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label="رمزعبور جدید",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="تایید رمز عبور جدید",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', )
        widgets = {
            'receiver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddReturnedOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order_id', None)
        super(AddReturnedOrderForm, self).__init__(*args, **kwargs)
        self.fields['products'].queryset = OrderProduct.objects.filter(order=self.order)


    class Meta:
        model = ReturnOrder
        fields = ['products', 'description']
        widgets = {
            'products': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control',
                                                                   'style': 'height:100px!important'}),
        }
