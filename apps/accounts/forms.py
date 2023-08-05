from django import forms
from .models import User, OTPCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='رمزعبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمزعبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('profile_img', 'first_name', 'last_name', 'phone_number', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('passwords dont match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>.", label='رمزعبور')

    class Meta:
        model = User
        fields = ('profile_img', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'last_login')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('رمز عبور و تایید رمز عبور یکسان نیست')
        return confirm_password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('شماره تلفن قبلا ثبت نام کرده')
        return phone_number


class LoginForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            return phone_number
        register_page = reverse('accounts:register')
        raise ValidationError(f'حسابی با شماره تلفن مورد نظر موجود نیست،'
                              f' <a href="{register_page}">ساخت حساب کاربری</a>')
