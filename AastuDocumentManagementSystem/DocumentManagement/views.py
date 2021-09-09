import os

from django.contrib import auth, messages
from django.http import FileResponse
from django.shortcuts import redirect, render

from .forms import (OfficeForm, ReplyMessageForm, SendMessageForm, SignInForm,
                    SignUPForm, TypeForm)
from .models import Message, Office, ReplyMessage, Type, User

##########################PDF Rendering #########################


def pdf_rendering():
    filepath = os.path.join('static', 'ProposalWriting.pdf')
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


################### Create Messages for user ####################


def send_messages(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        form = SendMessageForm()
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        if request.method == 'POST':
            form = SendMessageForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                category = cd['file'].content_type.split('/')[0].capitalize()
                users = User.objects.filter(office__office_name=cd['office'])
                carbon_copies = Office.objects.filter(
                    office_name=cd['cc_office'])
                users = users + carbon_copies
                for user in users:
                    send = Message(
                        message_description=cd['description'],
                        message_file=cd['file'],
                        message_sender=request.user,
                        message_receiver=user,
                        message_carbon_copy=True if user in carbon_copies else False
                    )
                    send.message_file.field.upload_to = f"{cd['office']}/{user}/{category}"
                    send.save()
        return render(request, 'create-send-message.html',
                      {'forms': form, 'notifications': notifications, 'count': count})

################### Reply Message for received message #############


def reply_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        msg = Message.objects.get(message_id=message_id)
        type_name = request.user.office.office_type_name
        office = request.user.office
        form = ReplyMessageForm()
        if request.method == 'POST':
            form = ReplyMessageForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                category = cd['file'].content_type.split('/')[0].capitalize()
                users = User.objects.filter(office__office_name=cd['office'])
                carbon_copies = Office.objects.filter(
                    office_name=cd['cc_office'])
                users = users + carbon_copies
                for user in users:
                    send = ReplyMessage(
                        reply_description=cd['description'],
                        reply_file=cd['file'],
                        reply_sender=request.user,
                        reply_receiver=user,
                        reply_carbon_copy=True if user in carbon_copies else False,
                        replyed_message=msg
                    )
                    send.reply_file.field.upload_to = f"{cd['office']}/{user}/{category}"
                    send.save()
        return render(request, 'create-send-message.html',
                      {'forms': form, 'type_name': type_name, 'office': office, 'notifications': notifications, 'count': count})


################## Show Message ############################
def show_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        msg = Message.objects.get(message_id=message_id)
        count = notifications.count()
        return render(request, 'show_message.html', {'msg': msg, 'notifications': notifications, 'count': count})


################### Show all messages ########################
def show_all_message(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        messages = request.user.receiver.all()
        user = request.user
        count = notifications.count()
    return render(request, 'show_all_message.html', {'messages': messages, 'user': user, 'notifications': notifications, 'count': count})


################### Create Roles #############################
def create_types(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        form = TypeForm()
        if request.method == 'POST':
            form = TypeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data

                role = Type.objects.create(type_name=cd['type_name'])
                role.save()

    return render(request, 'create-role.html', {'forms': form, 'notifications': notifications, 'count': count})


def display_types(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        types = Type.objects.all()
        return render(request, 'display-types.html', {'types': types, 'notifications': notifications, 'count': count})
################### Create Offices #############################


def create_offices(request, type_id):

    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        form = OfficeForm()

        if request.method == 'POST':

            form = OfficeForm(request.POST)
            form1 = Type.objects.get(pk=type_id)
            if form.is_valid():
                cd = form.cleaned_data
                if Type.objects.filter(type_name=cd):
                    type_id = Type.objects.all()
                    office = Office.objects.create(
                        office_type_name_id=1, office_name=cd['office'])
                    office.save()

        return render(request, 'create-office.html', {'forms': form, 'notifications': notifications, 'count': count})


def display_offices(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        office = Office.objects.all()
        return render(request, 'display-offices.html', {'offices': office, 'notifications': notifications, 'count': count})

################### User Management #############################


def users(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        user = User.objects.all()
        return render(request, 'tables.html', {'user': user, 'notifications': notifications, 'count': count})


def create_users(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
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

        return render(request, 'create-users.html', {'forms': form, 'error': error, 'notifications': notifications, 'count': count})
############# Index User Dashboard###############################


def index(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        user = User.objects.get(id=request.user.id)
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        return render(request, 'index.html', {'user': user, 'notifications': notifications, 'count': count})


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
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(
                request, username=cd['username'], password=cd['password'])
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
