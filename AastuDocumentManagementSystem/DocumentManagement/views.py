import os

from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.http import FileResponse
# from django.contrib.auth import authenticate, login
#from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import (OfficeForm, SendMessageForm, SignInForm, SignUPForm,
                    TypeForm)
from .models import Document, Office, SendMessage, Type, User


##########################PDF Rendering #########################
def pdf_rendering(request):
    filepath = os.path.join('static', 'ProposalWriting.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
################### Create Messages for user ####################


def send_messages(request):
    form = SendMessageForm()
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            send = SendMessage(message_type_name=cd['type_name'],
                               message_office=cd['office'],
                               message_cc_type_name=cd['cc_type_name'],
                               message_cc_office=cd['cc_office'],
                               message_description=cd['description'],
                               message_file=cd['file'])
            send.save()
    return render(request, 'create-send-message.html', {'forms': form})


################### Create Roles #############################
def create_types(request):
    form = TypeForm()
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            role = Type.objects.create(type_name=cd['type_name'])
            role.save()

    return render(request, 'create-role.html', {'forms': form})


def display_types(request):
    types = Type.objects.all()
    print("Type:", types.__dict__)
    return render(request, 'display-types.html', {'types': types})
################### Create Offices #############################


def create_offices(request, type_id):

    form = OfficeForm()

    if request.method == 'POST':

        form = OfficeForm(request.POST)
        form1 = Type.objects.get(pk=type_id)
        print('Form:', form.__dict__)

        print('Form1:', form1)
        if form.is_valid():
            print("Office")
            cd = form.cleaned_data
            for t in cd:
                print(t['type_name'])
            if Type.objects.filter(type_name=cd):
                type_id = Type.objects.all()
                print("Office", type_id.__dict__)
                office = Office.objects.create(
                    office_type_name_id=1, office_name=cd['office'])
                office.save()

    return render(request, 'create-office.html', {'forms': form})


def display_offices(request):
    office = Office.objects.all()
    print("Office:", Office.__dict__)
    return render(request, 'display-offices.html', {'offices': office})


################### User Management #############################
def users(request):
    user = User.objects.all()
    print("User:", user.__dict__)

    return render(request, 'tables.html', {'user': user})


def create_users(request):
    string = "."
    form = SignUPForm()
    print('Form:', request)
    if request.method == "POST":
        form = SignUPForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['username'] = f"{cd['first_name']}.{cd['last_name']}"
            cd['password'] = cd['username']
            if User.objects.filter(username=cd['username']):
                error = 'Username is already taken!'
            else:
                del cd['submit']
                u = User.objects.create_user(**{i: cd[i] for i in cd})
                return redirect('signin')
        else:
            error = 'Please enter valid information'
        form = DocumentForm(request.POST)
        print(form)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            doc = Document(**{i: cd[i] for i in cd})
            doc.save()
            return redirect('doc')
    return render(request, 'create-document.html', {'forms': form})

    return render(request, 'create-users.html', {'forms': form})
############# Index User Dashboard###############################


def index(request):
    error = ''
    if not request.user.is_authenticated:
        return redirect('signin')
    else:

        print("User:", request.user.id)
        user = User.objects.get(id=request.user.id)
        print("User-1", user.__dict__)
        return render(request, 'index.html', {'user': user})


############ User Authentication Methods ########################

        #user = User.objects.get()
        return render(request, 'index.html')


def signup(request):
    error = ''
    form = SignUPForm()
    if request.method == "POST":
        form = SignUPForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['conf_password']:
                if User.objects.filter(username=cd['username']):
                    error = 'Username is already taken!'

                elif User.objects.filter(email=cd["email"]):
                    error = 'Email is already taken'
                else:
                    del cd['conf_password']
                    del cd['submit']
                    u = User.objects.create_user(**{i: cd[i] for i in cd})
                    u.save()
                    return redirect('signin')
            else:
                error = 'Password does not match!'
        else:
            error = 'Please enter valid information'
    return render(request, 'sign-up.html', {'forms': form, 'error': error})


def signin(request):
    error = ''
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        print("Form:", form)
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(
                request, username=cd['username'], password=cd['password'])
            print("User:", user)
            if user:
                auth.login(request, user)
                messages.info(
                    request, f"You are now logged in as {cd['username']}.")
                return redirect('index')
            else:
                error = 'Username or password is incorrect!'
        else:
            error = 'Please enter valid information'
    return render(request, 'sign-in.html', {'forms': form, 'error': error})


def signout(request):
    auth.logout(request)
    messages.info(request, f"You are now logged out.")
    if not request.user.is_authenticated:
        return redirect('signin')


def sendEmail(to, subject, body):
    import smtplib
    from email.message import EmailMessage
    msg = EmailMessage()
    gmail_user = 'aastudocumentationsystem@gmail.com'
    gmail_password = 'aastudocumentation123'
    msg['From'] = gmail_user
    msg['to'] = to
    msg['subject'] = subject
    msg.set_content(body)
    try:
        smtp_server = smtplib.SMTP_SSL(
            'smtp.gmail.com', 465)
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.send_message(msg)
        smtp_server.quit()
    except Exception as e:
        print(e)
    return redirect('/dms-app/signin')
