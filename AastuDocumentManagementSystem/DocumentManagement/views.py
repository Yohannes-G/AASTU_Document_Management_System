from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (ConfirmationForm, NewPasswordForm, ResetForm, SignInForm,
                    SignUPForm)
from .models import ConfirmationCode
from .models import User as U


def index(request):
    return render(request, 'index.html')


def signup(request):
    error = ''
    form = SignUPForm()
    if request.method == "POST":
        form = SignUPForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['conf_password']:
                try:
                    User.objects.get(username=cd['username'])
                    error = 'Username is already taken!'
                except User.DoesNotExist:
                    User.objects.create_user(
                        cd['username'], password=cd['password'])
                    return redirect('login')
            else:
                error = 'Password does not match!'
        else:
            error = 'Please enter valid information'
    return render(request, 'sign-up.html', {'forms': form, 'error': error})


def login(request):
    error = ''
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(
                username=cd['email'], password=cd['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                error = 'Username or password is incorrect!'
        else:
            error = 'Please enter valid information'
    return render(request, 'sign-in.html', {'forms': form, 'error': error})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('index')


def resetPassword(request):
    error = ''
    form = ResetForm()
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = U.objects.filter(user_email=cd['email'])
            if result:
                if not checkEmailAvailability(cd['email']):
                    import random
                    body = str(int(random.random() * 10000))
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
    form = ConfirmationForm()
    error = ''
    if request.method == "POST":
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            confirmation_code = checkEmailAvailability(email)
            if cd['confirmation'] == confirmation_code.confirmation_code:
                return redirect('newPassword', email=email)
            else:
                error = "Please enter the sent confirmation code"
        else:
            error = "Please enter valid information"
    return render(request, 'reset.html', {'forms': form, 'error': error})


def newPassword(request, email):
    form = NewPasswordForm()
    error = ''
    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['conf_password']:
                u = U.objects.get(user_email=email)
                u.user_password = cd['password']
                u.save()
                ConfirmationCode.objects.get(
                    user_email=email).delete()
                return redirect('login')
            else:
                error = "Password doesn't match"
        else:
            error = "Please enter valid information"
    return render(request, 'reset.html', {'forms': form, 'error': error})


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
    return redirect('/dms-app/login')
