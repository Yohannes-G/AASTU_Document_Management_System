from .models import Address
import json
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


class TypeForm(forms.Form):
    type_name = formGenerator('text', 'user', 'type')
    submit = formGenerator('submit', value='Create type')


class OfficeForm(forms.Form):
    type_name = forms.ModelChoiceField(queryset=Type.objects.all(),
                                       widget=forms.Select(
                                           attrs={'class': 'form-control1', }, ),
                                       empty_label="Select Type")

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

##################################################################################
def readJson(filename):
    with open(filename, 'r') as fp:
        return json.load(fp)


def get_country():
    """ GET COUNTRY SELECTION """
    filepath = './static/data/countries_states_cities.json'
    all_data = readJson(filepath)
    all_countries = [('-----', '---Select a Country---')]
    for x in all_data:
        y = (x['name'], x['name'])
        # print(y)
        all_countries.append(y)
    return all_countries


def return_state_by_country(country):
    """ GET STATE SELECTION BY COUNTRY INPUT """
    filepath = './static/data/countries_states_cities.json'
    all_data = readJson(filepath)

    all_states = []

    for x in all_data:
        print(x)
        if x['name'] == country:
            if 'states' in x:
                for state in x['states']:
                    y = (state['name'], state['name'])
                    all_states.append(state['name'])
            else:
                all_states.append(country)
    return all_states


class AddressForm(forms.ModelForm):
    country = forms.ChoiceField(
        choices=get_country(),
        required=False,
        label='Company Country Location',
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'id_country'}),
    )

    class Meta:
        model = Address
        fields = ['country']
####################################################


def get_type():
    """ GET Type SELECTION """
    all_countries = [('-----', '---Select a Type---')]
    all_data = [type_name.type_name for type_name in Type.objects.all()]
    #print("all_data", all_data)
    for x in all_data:
        y = (x, x)
        all_countries.append(y)
    return all_countries


class SignUPForm(forms.Form, forms.ModelForm):
    first_name = formGenerator('text', 'user', 'First Name')
    last_name = formGenerator('text', 'user', 'Last Name')
    type_name = forms.ChoiceField(choices=get_type(),
                                  widget=forms.Select(
                                      attrs={'class': 'form-control', 'id': 'id_type'})
                                  )
    submit = formGenerator('submit', value="Create User")

    class Meta:
        model = User
        fields = ['type_name']
