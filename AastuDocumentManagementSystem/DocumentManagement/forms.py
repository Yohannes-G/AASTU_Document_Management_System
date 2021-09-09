from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# from bootstrap_daterangepicker import widgets, fields
from .models import Office, Type, User


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
    username = formGenerator('text', 'user', 'Username')
    password = formGenerator('password', 'lock', 'Password')
    submit = formGenerator('submit', value="Login to your account")


class SignUPForm(forms.Form):
    first_name = formGenerator('text', 'user', 'First Name')
    last_name = formGenerator('text', 'user', 'Last Name')
    type_name = forms.ChoiceField(
        choices=(('President', 'President'),
                 ('Vice President', 'Vice President')),
        widget=forms.Select(attrs={
            'class': 'form-control1',
        }, ), label=''
    )
    office = forms.ChoiceField(
        choices=(('Electrical Engineering', 'Electrical Engineering'),
                 (' Mechanical Engineering', 'Mechanical Engineering')),
        widget=forms.Select(attrs={
            'class': 'form-control1',
        }, ), label=''
    )
    submit = formGenerator('submit', value="Create User")


class TypeForm(forms.Form):
    type_name = formGenerator('text', 'user', 'type')
    submit = formGenerator('submit', value='Create type')


class OfficeForm(forms.Form):
    type_name = forms.ModelChoiceField(
        queryset=Type.objects.all(), empty_label="Selected value")
    office = formGenerator('text', 'user', 'office')
    submit = formGenerator('submit', value='Create Office')


class ReplyMessageForm(forms.Form):
    cc_type_name = forms.ChoiceField(
        choices=(('President', 'President'),
                 ('Vice President', 'Vice President')),
        widget=forms.Select(attrs={
            'class': 'form-control1',
        }, ), label=''
    )
    cc_office = forms.ChoiceField(
        choices=(('Electrical Engineering', 'Electrical Engineering'),
                 (' Mechanical Engineering', 'Mechanical Engineering')),
        widget=forms.Select(attrs={
            'class': 'form-control1',
        }, ), label=''
    )
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'user',
        'placeholder': 'description',
    }), label='')

    file = forms.FileField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'type': 'file',
    }
    ), label='')

    submit = formGenerator('submit', value="Send File")


class SendMessageForm(ReplyMessageForm):
    type_name = forms.ChoiceField(
        choices=(('President', 'President'),
                 ('Vice President', 'Vice President')),
        widget=forms.Select(attrs={
            'class': 'form-control1',
        }, ), label=''
    )
    office = forms.ChoiceField(
        choices=(('Electrical Engineering', 'Electrical Engineering'),
                 (' Mechanical Engineering', 'Mechanical Engineering')),
        widget=forms.Select(attrs={
            'class': 'form-control1',
        }, ), label=''
    )

    field_order = ['type_name', 'office']


# class ResetForm(forms.Form):
#     email = formGenerator('email', 'email', 'Email Address')
#     submit = formGenerator('submit', value="Reset")


# class ConfirmationForm(forms.Form):
#     confirmation = formGenerator('text', 'lock', 'Confirmation')
#     submit = formGenerator('submit', value="Confirm")


# class NewPasswordForm(forms.Form):
#     password = formGenerator('password', 'lock', 'Password')
#     conf_password = formGenerator('password', 'lock', 'Confirm Password')
#     submit = formGenerator('submit', value="Submit")
