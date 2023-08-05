from django import forms
from .models import Order, ReturnOrder


class OrderForm(forms.ModelForm):
    receiver_extra_data = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '40', 'rows': '3'}), label='توضیحات اضافه')
    post_price = forms.IntegerField(
        widget=forms.NumberInput(attrs={'style': 'width:min(100%, 700px)'}), label='هزینه پست')

    class Meta:
        model = Order
        fields = '__all__'


class ReturnOrderForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '40', 'rows': '3'}), label='توضیحات')

    class Meta:
        model = ReturnOrder
        fields = '__all__'
