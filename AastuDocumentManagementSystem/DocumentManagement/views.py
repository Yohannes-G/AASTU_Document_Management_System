import os

from django.contrib import auth, messages
<<<<<<< HEAD
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import (ConfirmationForm, NewPasswordForm, ResetForm, SignInForm,
                    SignUPForm, TypeForm, OfficeForm, SendMessageForm)
from .models import User, Type, Office,SendMessage
=======
>>>>>>> 9723e0191e65e74b324798e7bdbc65858dda87ac
from django.http import FileResponse
from django.shortcuts import redirect, render

from .forms import (OfficeForm, SendMessageForm, SignInForm, SignUPForm,
                    TypeForm)
from .models import Message, Office, Type, User


##########################PDF Rendering #########################
def pdf_rendering(request):
    filepath = os.path.join('static', 'ProposalWriting.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
################### Create Messages for user ####################


def send_messages(request):
    form = SendMessageForm()
    if request.method == 'POST':
        form = SendMessageForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            category = cd['file'].content_type.split('/')[0].capitalize()
            users = User.objects.filter(office__office_name=cd['office'])
            send = Message(
                message_description=cd['description'],
                message_file=cd['file'],
                message_sender=request.user)
            send.message_file.field.upload_to = f"{cd['office']}/{category}"
            send.save()
            send.message_receiver.add(*users)
    return render(request, 'create-send-message.html', {'forms': form})


################## Show Message ############################
def show_message(request, message_id):
    msg = Message.objects.get(message_id=message_id)
    return render(request, 'show_message.html', {'msg': msg})


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
    print('Request:', request.POST)
    types = Type.objects.all()
    offices = Office.objects.all()
    print("Offices:", offices.__dict__)
    print("Type:", types.__dict__)
<<<<<<< HEAD
    return render(request, 'display-types.html', {'types':types })
=======
    return render(request, 'display-types.html', {'types': types})
>>>>>>> 9723e0191e65e74b324798e7bdbc65858dda87ac
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
<<<<<<< HEAD
            office = Office.objects.create(office_type_name_id=type_id, office_name=cd['office'])
            office.save()

    return render(request, 'create-office.html', {'forms':form, 'type_id':type_id})

def display_offices(request, type_id):
    office = Office.objects.filter(office_type_name_id=type_id)

    return render(request, 'display-offices.html', {'offices': office, 'type_id':type_id})
=======
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
>>>>>>> 9723e0191e65e74b324798e7bdbc65858dda87ac

################### User Management #############################


def users(request):
    user = User.objects.all()
    print("User:", user.__dict__)

    return render(request, 'tables.html', {'user': user})


def create_users(request):
    error = ""
    form = SignUPForm()
    if request.method == "POST":
        form = SignUPForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['username'] = f"{cd['first_name']}.{cd['last_name']}"
            cd['password'] = cd['username']
            cd['office'] = Office.objects.get(office_name=cd['office'])
            if User.objects.filter(username=cd['username']):
                error = 'Username is already taken!'
            else:
                del cd['submit']
                del cd['type_name']
                u = User.objects.create_user(**{i: cd[i] for i in cd})
                u.save()
                return redirect('signin')
        else:
            error = 'Please enter valid information'

    return render(request, 'create-users.html', {'forms': form, 'error': error})
############# Index User Dashboard###############################


def index(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
<<<<<<< HEAD
        print("User:",request.user.id)
=======
>>>>>>> 9723e0191e65e74b324798e7bdbc65858dda87ac
        user = User.objects.get(id=request.user.id)
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        return render(request, 'index.html', {'user': user, 'notifications': notifications, 'count': count})

<<<<<<< HEAD
=======

############ User Authentication Methods ########################
>>>>>>> 9723e0191e65e74b324798e7bdbc65858dda87ac
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


# def resetPassword(request):
#     error = ''
#     form = ResetForm()
#     if request.method == "POST":
#         form = ResetForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             result = User.objects.filter(email=cd['email'])
#             if result:
#                 if not checkEmailAvailability(cd['email']):
#                     import random
#                     body = str(int(random.randint(1000, 9999)))
#                     sendEmail(to=cd['email'], subject="Reset Password",
#                               body=f'The confirmation code to reset your password is {body}')
#                     u = ConfirmationCode(user=result[0],
#                                          user_email=cd['email'],
#                                          confirmation_code=body)
#                     u.save()

#                 return redirect("confirmation", email=cd['email'])
#             else:
#                 error = "You have no account with this email"
#         else:
#             error = "Please enter valid information"
#     return render(request, 'reset.html', {'forms': form, 'error': error})


# def confirmation(request, email):
#     confirmation_code = checkEmailAvailability(email)
#     if confirmation_code:
#         form = ConfirmationForm()
#         error = ''
#         if request.method == "POST":
#             form = ConfirmationForm(request.POST)
#             if form.is_valid():
#                 cd = form.cleaned_data
#                 if cd['confirmation'] == confirmation_code.confirmation_code:
#                     return redirect('newPassword', email=email)
#                 else:
#                     error = "Please enter the sent confirmation code"
#             else:
#                 error = "Please enter valid information"
#         return render(request, 'reset.html', {'forms': form, 'error': error})
#     else:
#         return redirect('signin')


# def newPassword(request, email):

#     try:
#         confirm = ConfirmationCode.objects.get(
#             user_email=email)
#         form = NewPasswordForm()
#         error = ''
#         if request.method == "POST":
#             form = NewPasswordForm(request.POST)
#             if form.is_valid():
#                 cd = form.cleaned_data
#                 if cd['password'] == cd['conf_password']:
#                     u = User.objects.get(email=email)
#                     u.user_password = cd['password']
#                     u.save()
#                     confirm.delete()
#                     return redirect('signin')
#                 else:
#                     error = "Password doesn't match"
#             else:
#                 error = "Please enter valid information"
#         return render(request, 'reset.html', {'forms': form, 'error': error})
#     except:
#         return redirect('signin')


# def checkEmailAvailability(email):
#     try:
#         confirmation_code = ConfirmationCode.objects.get(user_email=email)
#         return confirmation_code
#     except:
#         return False


# def sendEmail(to, subject, body):
#     import smtplib
#     from email.message import EmailMessage
#     msg = EmailMessage()
#     gmail_user = 'aastudocumentationsystem@gmail.com'
#     gmail_password = 'aastudocumentation123'
#     msg['From'] = gmail_user
#     msg['to'] = to
#     msg['subject'] = subject
#     msg.set_content(body)
#     try:
#         smtp_server = smtplib.SMTP_SSL(
#             'smtp.gmail.com', 465)
#         smtp_server.login(gmail_user, gmail_password)
#         smtp_server.send_message(msg)
#         smtp_server.quit()
#     except Exception as e:
#         print(e)
#     return redirect('/dms-app/signin')
