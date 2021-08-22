from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ConfirmationForm, NewPasswordForm, ResetForm
from .models import ConfirmationCode
from .models import User as U


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'sign-up.html', {'error': 'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('/dms-app/index')
        else:
            return render(request, 'sign-up.html', {'error': 'Password does not match!'})
    else:
        return render(request, 'sign-up.html')


def login(request):
    if request.method == 'POST':
        print("-------------------")
        print(request.POST['password1'])
        user = auth.authenticate(
            username=request.POST['username'], password=request.POST['password1'])
        if user is not None:
            auth.login(request, user)
            return redirect('/dms-app/index')
        else:
            return render(request, 'sign-in.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'sign-in.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('/')


def resetPassword(request):
    form = ResetForm()
    if request.method == "POST":
        form = ResetForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = U.objects.filter(user_email=cd['user_email']).values()
            if result:
                if not checkEmailAvailability(cd['user_email']):
                    # import random
                    # body = str(random.random() * 10000)
                    # sendEmail(to=cd['user_email'], subject="Reset Password", body=f'The confirmation code to reset your password is {body}')
                    body = "4567"
                    u = ConfirmationCode(user=result[0],
                                         user_email=cd['user_email'],
                                         confirmation_code=body)
                    u.save()

                return redirect("confirmation", email=cd['user_email'])
    return render(request, 'reset.html', {'form': form, 'value': "Reset"})


def confirmation(request, email):
    form = ConfirmationForm()
    if request.method == "POST":
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            confirmation_code = checkEmailAvailability(email)
            if cd['confirmation'] == confirmation_code.confirmation_code:
                return redirect('newPassword', email=email)
    return render(request, 'reset.html', {'form': form, 'value': 'Confirm'})


def newPassword(request, email):
    form = NewPasswordForm()
    msg = ''
    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['user_password'] == cd['user_confirm_password']:
                u = U.objects.get(user_email=email)
                u.user_password = cd['user_password']
                u.save()
                ConfirmationCode.objects.get(
                    user_email=email).delete()
                redirect('login')
            else:
                msg = 'please make sure confirmation password is similar to new password'
    return render(request, 'reset.html', {'form': form, 'value': "Submit", 'msg': msg})


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
