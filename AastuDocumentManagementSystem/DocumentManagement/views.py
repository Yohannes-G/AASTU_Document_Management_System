from django.contrib import auth, messages
# from django.contrib.auth import authenticate, login
#from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (ConfirmationForm, DocumentForm, NewPasswordForm, ResetForm,
                    SignInForm, SignUPForm)
from .models import ConfirmationCode, Document, User


def doc(request):
    form = DocumentForm()
    if request.method == "POST":
        form = DocumentForm(request.POST)
        print(form)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            doc = Document(**{i: cd[i] for i in cd})
            doc.save()
            return redirect('doc')
    return render(request, 'create-document.html', {'forms': form})


def index(request):
    error = ''
    if not request.user.is_authenticated:
        return redirect('signin')
    else:

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
