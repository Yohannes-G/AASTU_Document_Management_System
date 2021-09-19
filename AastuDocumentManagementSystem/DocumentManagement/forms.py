from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# from bootstrap_daterangepicker import widgets, fields
from .models import MyProfile, Office, Type, User


def formGenerator(tpe, cls='', placeholder='', value=''):
    return forms.CharField(widget=forms.TextInput(attrs={
        'class': cls,
        'type': tpe,
        'placeholder': placeholder,
        'value': value
    }), label='')


# def get_type(default='-----', value='---Select a Type---'):
#     """ GET Type SELECTION """
#     all_countries = [(value, default)]
#     all_data = [type_name.type_name for type_name in Type.objects.all()]
#     #print("all_data", all_data)
#     for x in all_data:
#         y = (x, x)
#         all_countries.append(y)
#     return all_countries


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


class TypeForm(forms.Form):
    type_name = formGenerator('text', 'user', 'type')
    submit = formGenerator('submit', value='Create type')


class OfficeForm(forms.Form):
    office = formGenerator('text', 'user', 'office')
    submit = formGenerator('submit', value='Create Office')


class ReplyMessageForm(forms.Form):
    pass
    # cc_type_name = forms.ChoiceField(choices=get_type(),
    #                                  widget=forms.Select(
    #     attrs={'class': 'form-control', 'id': 'id_cc_type'})
    # )
    # description = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'user',
    #     'placeholder': 'description',
    # }), label='')

    # file = forms.FileField(required=False, widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'type': 'file',
    # }
    # ), label='')

    # submit = formGenerator('submit', value="Send File")


class SendMessageForm(forms.Form):
    pass
    # type_name = forms.ChoiceField(choices=get_type(),
    #                               widget=forms.Select(
    #                                   attrs={'class': 'form-control', 'id': 'id_type'})
    #                               )
    # cc_type_name = forms.ChoiceField(choices=get_type(),
    #                                  widget=forms.Select(
    #     attrs={'class': 'form-control', 'id': 'id_cc_type'})
    # )
    # description = forms.CharField(widget=forms.Textarea(attrs={
    #     'class': 'user',
    #     'placeholder': 'description',
    # }), label='')

    # file = forms.FileField(required=False, widget=forms.TextInput(attrs={
    #     'class': 'form-control',
    #     'type': 'file',
    # }
    # ), label='')

    # submit = formGenerator('submit', value="Send File")

    # field_order = ['type_name', 'office']


class MessageFilterForm(forms.Form):
    pass
    # type_name = forms.ChoiceField(choices=get_type(default="---All---", value="All"),
    #                               widget=forms.Select(
    #                                   attrs={'class': 'form-control', 'id': 'id_type'})
    #                               )
    # action = forms.ChoiceField(choices=[("0", "Both"), ("1", "Receive"), ("2", "Send")], widget=forms.Select(
    #     attrs={'class': 'form-control', 'id': 'id_type'}))


class NotificationFilterForm(MessageFilterForm):
    pass
    # to_type_name = forms.ChoiceField(
    #     choices=get_type(default="---All---", value="All"),
    #     widget=forms.Select(
    #         attrs={'class': 'form-control', 'id': 'id_to_type'})
    # )


class ResetForm(forms.Form):
    email = formGenerator('email', 'email', 'Email Address')
    submit = formGenerator('submit', value="Reset")


class ConfirmationForm(forms.Form):
    confirmation = formGenerator('text', 'lock', 'Confirmation')
    submit = formGenerator('submit', value="Confirm")


class NewPasswordForm(forms.Form):
    password = formGenerator('password', 'lock', 'Password')
    conf_password = formGenerator('password', 'lock', 'Confirm Password')
    submit = formGenerator('submit', value="Submit")


class SignUPForm(forms.Form, forms.ModelForm):
    pass
    # first_name = formGenerator('text', 'user', 'First Name')
    # last_name = formGenerator('text', 'user', 'Last Name')
    # type_name = forms.ChoiceField(choices=get_type(),
    #                               widget=forms.Select(
    #                                   attrs={'class': 'form-control', 'id': 'id_type'}),
    #                               label='Select User Type'
    #                               )
    # submit = formGenerator('submit', value="Create User")

    # class Meta:
    #     model = User
    #     fields = ['type_name']


class UpdateUserForm(forms.Form, forms.ModelForm):
    username = formGenerator('text', 'user', 'Username')
    submit = formGenerator('submit', value="Save")

    class Meta:
        model = User
        fields = ['username']


class ProfileForm(forms.Form, forms.ModelForm):
    profile_image = forms.ImageField()
    submit = formGenerator('submit', value="Save")

    class Meta:
        model = MyProfile
        fields = ['profile_image']
