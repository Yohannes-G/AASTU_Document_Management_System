from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


def formGenerator(tpe, cls='', placeholder='', value=''):
    return forms.CharField(widget=forms.TextInput(attrs={
        'class': cls,
        'type': tpe,
        'placeholder': placeholder,
        'value': value
    }), label='')


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class SignInForm(forms.Form):
    email = formGenerator('text', 'user', 'Email Address')
    password = formGenerator('password', 'lock', 'Password')
    submit = formGenerator('submit', value="Login to your account")


class SignUPForm(forms.Form):
    first_name = formGenerator('text', 'user', 'First Name')
    last_name = formGenerator('text', 'user', 'Last Name')
    sex = forms.ChoiceField(
        choices=(('Male', 'Male'), ('Female', 'Female')),
        widget=forms.Select(attrs={
            'class': 'form-control1',
        }, ), label=''
    )
    username = formGenerator('text', 'user', 'Username')
    email = formGenerator('email', 'user', 'Email Address')
    password = formGenerator('password', 'lock', 'Password')
    conf_password = formGenerator('password', 'lock', 'Confirm Password')
    submit = formGenerator('submit', value="Submit")


class ResetForm(forms.Form):
    email = formGenerator('email', 'user', 'Email Address')
    submit = formGenerator('submit', value="Reset")


class ConfirmationForm(forms.Form):
    confirmation = formGenerator('text', 'lock', 'Confirmation')
    submit = formGenerator('submit', value="Confirm")


class NewPasswordForm(forms.Form):
    password = formGenerator('password', 'lock', 'Password')
    conf_password = formGenerator('password', 'lock', 'Confirm Password')
    submit = formGenerator('submit', value="Submit")
