from django import forms

from .models import User


class ResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_email']


class ConfirmationForm(forms.Form):
    confirmation = forms.CharField(max_length=4)


class NewPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_password', 'user_confirm_password']
