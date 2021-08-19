from django import forms

from .models import User


class SignInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_email', 'user_password']
