from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
<<<<<<< HEAD
from django.urls import reverse
from django.contrib.auth import authenticate, login
from .forms import (ConfirmationForm, NewPasswordForm, ResetForm, SignInForm,
                    SignUPForm, DocumentForm)
from .models import ConfirmationCode, Document
#from .models import User
=======

from .forms import (ConfirmationForm, NewPasswordForm, ResetForm, SignInForm,
                    SignUPForm)
from .models import ConfirmationCode, User
>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f

def doc(request):
    form = DocumentForm()
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            doc = Document(**{i:cd[i] for i in cd})
            doc.save()
            return redirect('doc')
    return render(request, 'create-document.html', {'forms':form})

def index(request):
<<<<<<< HEAD
    error=''
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        
        #user = User.objects.get()
        return render(request, 'index.html')

#cd->clean data
=======
    if request.user.is_authenticated:
        return render(request, 'index.html')
    return redirect('signin')


>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f
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
<<<<<<< HEAD
                except User.DoesNotExist:
                    del cd["conf_password"]
                    del cd["submit"]
                    del cd["sex"]
                    u = User.objects.create_user(**{i:cd[i] for i in cd})
                    messages.info(request, f"You are Registered in as {username}.")
                    u.save()
                        #cd['user_username'], user_password=cd['user_password'])
=======
                elif User.objects.filter(email=cd["email"]):
                    error = 'Email is already taken'
                else:
                    del cd['conf_password']
                    del cd['submit']
                    u = User.objects.create_user(**{i: cd[i] for i in cd})
                    u.save()
>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f
                    return redirect('signin')
            else:
                error = 'Password does not match!'
        else:
            error = 'Please enter valid information'
    return render(request, 'sign-up.html', {'forms': form, 'error': error})

    


<<<<<<< HEAD

=======
>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f
def signin(request):
    error = ''
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
<<<<<<< HEAD
            username=request.POST["username"]
            password=request.POST["password"]
            print("Login:", username)
            print("Login:", password)
            user = authenticate( request,
                username=username, password=password)
            print("Authenticated", user)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
=======
            user = auth.authenticate(
                request, username=cd['email'], password=cd['password'])
            if user:
                auth.login(request, user)
>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f
                return redirect('index')
            else:
                error = 'Username or password is incorrect!'
        else:
            error = 'Please enter valid information'
    return render(request, 'sign-in.html', {'forms': form, 'error': error})


def signout(request):
    auth.logout(request)
<<<<<<< HEAD
    if not request.user.is_authenticated:
        return redirect('signin')
=======
    return redirect('signin')
>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f


def resetPassword(request):
    error = ''
    form = ResetForm()
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = User.objects.filter(user_email=cd['email'])
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
        redirect('login')


def newPassword(request, email):
<<<<<<< HEAD
    form = NewPasswordForm()
    error = ''
    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['conf_password']:
                u = User.objects.get(user_email=email)
                u.user_password = cd['password']
                u.save()
                ConfirmationCode.objects.get(
                    user_email=email).delete()
                return redirect('login')
=======
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
                    u = User.objects.get(user_email=email)
                    u.user_password = cd['password']
                    u.save()
                    confirm.delete()
                    return redirect('login')
                else:
                    error = "Password doesn't match"
>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f
            else:
                error = "Please enter valid information"
        return render(request, 'reset.html', {'forms': form, 'error': error})
    except:
        return redirect('login')


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
 