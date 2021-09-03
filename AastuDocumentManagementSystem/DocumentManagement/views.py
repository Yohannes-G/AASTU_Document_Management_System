from django.contrib import auth, messages
#from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import (ConfirmationForm, NewPasswordForm, ResetForm, SignInForm,
                    SignUPForm, TypeForm, OfficeForm, SendMessageForm)
from .models import User, Type, Office,SendMessage
from django.http import FileResponse
import os
##########################PDF Rendering #########################
def pdf_rendering(request):
    filepath=os.path.join('static', 'ProposalWriting.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
################### Create Messages for user ####################
def send_messages(request):
    form = SendMessageForm()
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            send = SendMessage( message_type_name=cd['type_name'],
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
    return render(request, 'display-types.html', {'types':types})
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
                type_id=Type.objects.all()
                print("Office", type_id.__dict__)
                office = Office.objects.create( office_type_name_id=1 ,office_name=cd['office'])
                office.save()

    return render(request, 'create-office.html', {'forms':form})

def display_offices(request):
    office = Office.objects.all()
    print("Office:", Office.__dict__)
    return render(request, 'display-offices.html', {'offices': office})

################### User Management #############################
def users(request):
    user = User.objects.all()
    print("User:",user.__dict__)

    return render(request, 'tables.html', {'user':user})

def create_users(request):
    string="."
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
                u = User.objects.create_user(**{i:cd[i] for i in cd})
                return redirect('signin')
        else:
            error = 'Please enter valid information'

    return render(request, 'create-users.html', {'forms': form})
############# Index User Dashboard###############################
def index(request):
    error=''
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        
        print("User:",request.user.id)
        user = User.objects.get(id=request.user.id)
        print("User-1",user.__dict__)
        return render(request, 'index.html', {'user': user})


############ User Authentication Methods ########################
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
            print("User:",user)
            if user:
                auth.login(request, user)
                messages.info(request, f"You are now logged in as {cd['username']}.")
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
 


def resetPassword(request):
    error = ''
    form = ResetForm()
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = User.objects.filter(email=cd['email'])
            if result:
                if not checkEmailAvailability(cd['email']):
                    import random
                    body = str(int(random.randint(1000, 9999)))
                    sendEmail(to=cd['email'], subject="Reset Password",
                              body=f'The confirmation code to reset your password is {body}')
                    u = ConfirmationCode(user=result[0],
                                         user_email=cd['email'],
                                         confirmation_code=body)
                    u.save()

                return redirect("confirmation", email=cd['email'])
            else:
                error = "You have no account with this email"
        else:
            error = "Please enter valid information"
    return render(request, 'reset.html', {'forms': form, 'error': error})


def confirmation(request, email):
    confirmation_code = checkEmailAvailability(email)
    if confirmation_code:
        form = ConfirmationForm()
        error = ''
        if request.method == "POST":
            form = ConfirmationForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if cd['confirmation'] == confirmation_code.confirmation_code:
                    return redirect('newPassword', email=email)
                else:
                    error = "Please enter the sent confirmation code"
            else:
                error = "Please enter valid information"
        return render(request, 'reset.html', {'forms': form, 'error': error})
    else:
        return redirect('signin')


def newPassword(request, email):

    try:
        confirm = ConfirmationCode.objects.get(
            user_email=email)
        form = NewPasswordForm()
        error = ''
        if request.method == "POST":
            form = NewPasswordForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                if cd['password'] == cd['conf_password']:
                    u = User.objects.get(email=email)
                    u.user_password = cd['password']
                    u.save()
                    confirm.delete()
                    return redirect('signin')
                else:
                    error = "Password doesn't match"
            else:
                error = "Please enter valid information"
        return render(request, 'reset.html', {'forms': form, 'error': error})
    except:
        return redirect('signin')


def checkEmailAvailability(email):
    try:
        confirmation_code = ConfirmationCode.objects.get(user_email=email)
        return confirmation_code
    except:
        return False


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
 