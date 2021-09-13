import json
import os

from django.contrib import auth, messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import (OfficeForm, ReplyMessageForm, SendMessageForm, SignInForm,
                    SignUPForm, TypeForm, ProfileForm)
from .models import Message, Office, ReplyMessage, Type, User, Profile

######################## Drop Down ##############################

# Functions for drop down menu

def get_type():
    """ GET Type SELECTION """
    all_countries = [('-----', '---Select a Type---')]
    all_data = [type_name.type_name for type_name in Type.objects.all()]
    #print("all_data", all_data)
    for x in all_data:
        y = (x, x)
        all_countries.append(y)
    return all_countries


def return_office_by_type(type_name):
    all_offices = []
    all_data = [type_name.type_name for type_name in Type.objects.all()]
    print(all_data)
    # get the id of the comming type
    typeId = Type.objects.get(type_name=type_name)
    #print("return:", typeId)

    for x in all_data:
       # print(x)
        if x == type_name:
            office_list = Office.objects.filter(
                office_type_name_id=typeId.type_id)
            #print("office_list", office_list)
            for office in office_list:
                #print("Office New:", office)
                y = (office, office)
                all_offices.append(office)
                #print("all_offices", all_offices)
    return all_offices


def getOffices(request):
    office_type_name = request.POST.get('type_name')
    #office_type_name = 'Director'
    #print("getOffices: ", office_type_name)
    offices = return_office_by_type(office_type_name)
    office = [office.office_name for office in offices]

    return JsonResponse(office,  safe=False)


# ##########################PDF Rendering #########################


# def pdf_rendering():
#     filepath = os.path.join('static', 'ProposalWriting.pdf')
#     return FileResponse(open(filepath, 'rb'), content_type='application/pdf')


################### Create Messages for User ####################


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
            selected_office = request.POST['state']
            selected_cc_office = request.POST['cc_state']

            print("messages: ", selected_office)
            print("messages: ", selected_cc_office)

            if form.is_valid():
                cd = form.cleaned_data
                print("messages: ", cd)
                category = request.FILES['file'].content_type.split(
                    '/')[-1].capitalize()
                users = list(User.objects.filter(
                    office__office_name=selected_office))
                carbon_copies = list(User.objects.filter(
                    office__office_name=selected_cc_office))
                users = users + carbon_copies
                for user in users:
                    send = Message(
                        message_description=cd['description'],
                        message_file=request.FILES['file'],
                        message_sender=request.user,
                        message_receiver=user,
                        message_cc=True if user in carbon_copies else False
                    )
                    send.message_file.field.upload_to = f"{selected_office}/{user.username}/{category}"
                    send.save()
                return redirect('sendmessages')
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
            selected_cc_office = request.POST['cc_state']
            if form.is_valid():
                cd = form.cleaned_data
<<<<<<< HEAD
                category = cd['file'].content_type.split('/')[0].capitalize()
                users = User.objects.filter(office__office_name=cd['office'])
                carbon_copies = Office.objects.filter(
                    office_name=selected_cc_office)
=======
                category = request.FILES['file'].content_type.split(
                    '/')[-1].capitalize()
                users = list(User.objects.filter(
                    office__office_name=office))
                carbon_copies = list(User.objects.filter(
                    office__office_name=cd['cc_office']))
>>>>>>> c7bde0b2c25224dd32a90eb7f44b5acddaaffaa5
                users = users + carbon_copies
                for user in users:
                    send = ReplyMessage(
                        reply_description=cd['description'],
                        reply_file=request.FILES['file'],
                        reply_sender=request.user,
                        reply_receiver=user,
                        reply_cc=True if user in carbon_copies else False,
                        replyed_message=msg
                    )
                    send.reply_file.field.upload_to = f"{office}/{user.username}/{category}"
                    send.save()
                return redirect('showallmessage')
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
        type_name = Type.objects.get(type_id=type_id)
        if request.method == 'POST':
            form = OfficeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                office = Office.objects.create(
                    office_type_name_id=type_id, 
                    office_name=cd['office'])
                office.save()
        return render(request, 'create-office.html', {'forms': form, 'notifications': notifications, 'count': count, 'type_id':type_id})

def display_offices(request, type_id):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        office = Office.objects.all()
        return render(request, 'display-offices.html', {'offices': office, 'notifications': notifications, 'count': count, 'type_id': type_id})

################### User Management #############################
def create_user_profile(request):
    error=' '
    form = ProfileForm()
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            print("Profile:", cd)
            print("User:", request.user.last_name)
            #request.user.username = cd['username']
            request.user.first_name = cd['edit_first_name']
            #request.user.last_name = cd['edit_last_name']
            # if cd['new_password'] == cd['confirm_password']:
            #     request.user.password = cd['new_password']
            # else:
            #     error = 'Please enter the correct password!'
            print("User:", request.user.first_name)
            profile = Profile.objects.create(
                    profile_user = user.id,
                    profile_image = cd['profile_image']
                )
            profile.save()

    return render(request, 'create-user-profile.html', {'forms':form, 'error':error, 'user':user})

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
    ty = Type.objects.all()
    off = Office.objects.all()

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
                #--------------------------------------------------------------
                off_id = Office.objects.get(office_name=request.POST['state'])
                selected_office = request.POST['state']

                cd = form.cleaned_data
               # print("This office: ",cd)
                cd['username'] = f"{cd['first_name']}.{cd['last_name']}"
                cd['password'] = cd['username']
                cd['office_id'] = off_id.office_id
                # ---------------------------------------------------------------
                if User.objects.filter(username=cd['username']):
                    error = 'Username is already taken!'
                else:
                    del cd['submit']
                    del cd['type_name']
                    u = User.objects.create_user(**{i: cd[i] for i in cd})
                    u.save()
                    return redirect('createusers')
            else:
                error = 'Please enter valid information'

        return render(request, 'create-users.html', {'forms': form, 'error': error, 'notifications': notifications, 'count': count})
############# Index User Dashboard###############################


def index(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        print("User:", request.user.id)
        user = User.objects.get(id=request.user.id)
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        return render(request, 'index.html', {'user': user, 'notifications': notifications, 'count': count})


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
