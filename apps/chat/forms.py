from django import forms
from .models import Comment


class CommentForm(forms.Form):
    reply_to = forms.CharField(widget=forms.HiddenInput(attrs={'value':'0', 'id': 'reply-to-field'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'comment-text'}), label='دیدگاه شما')


class CommentAdminForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': '3', 'cols': '40'}), label='متن پیام')

    class Meta:
        model = Comment
        fields = '__all__'
