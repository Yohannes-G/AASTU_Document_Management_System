import json
import os

from django.contrib import auth, messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import (OfficeForm, ReplyMessageForm, SendMessageForm, SignInForm,
                    SignUPForm, TypeForm, ProfileForm,UpdateUserForm, NewPasswordForm)
from .models import Message, Office, ReplyMessage, Type, User, MyProfile
from django.contrib.auth.hashers import make_password
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
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'create-send-message.html',
                      {'forms': form, 'notifications': notifications, 'count': count, 'profile':profile})

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
                category = request.FILES['file'].content_type.split(
                    '/')[-1].capitalize()
                users = list(User.objects.filter(
                    office__office_name=office))
                carbon_copies = list(User.objects.filter(
                    office__office_name=selected_cc_office))
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
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'create-send-message.html',
                      {'forms': form, 'type_name': type_name, 'office': office, 'notifications': notifications, 'count': count, 'profile':profile})


################## Show Message ############################
def show_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        msg = Message.objects.get(message_id=message_id)
        count = notifications.count()
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'show_message.html', {'msg': msg, 'notifications': notifications, 'count': count, 'profile':profile})


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
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'show_all_message.html', {'messages': messages, 'user': user,'profile':profile, 'notifications': notifications, 'count': count})


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
                messages.success(request, 'Type is Created!')
                role.save()
                return redirect('displaytypes')
    user = User.objects.get(id=request.user.id)
    if MyProfile.objects.filter(profile_user_id=user.id):
        profile = MyProfile.objects.get(profile_user_id=user.id)
    else:
        profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'create-role.html', {'forms': form,'profile':profile, 'notifications': notifications, 'count': count})


def display_types(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        types = Type.objects.all()
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'display-types.html', {'types': types, 'profile':profile, 'notifications': notifications, 'count': count})


def delete_types(request, type_id):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        typ = Type.objects.get(type_id=type_id)
        typ.delete()
        messages.error(request, 'Type deleted.')
        return redirect('displaytypes')

def edit_types(request, type_id):
    typ = Type.objects.get(type_id=type_id)
    form = TypeForm()
  
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Type.objects.filter(type_name=cd['type_name']):
                error = 'Type is already Created!'
            else:
                typ.type_name = cd['type_name']
                typ.save()
                return redirect('displaytypes')
        else:
            print(form.errors)
    user = User.objects.get(id=request.user.id)
    if MyProfile.objects.filter(profile_user_id=user.id):
        profile = MyProfile.objects.get(profile_user_id=user.id)
    else:
        profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'edit-types.html', {'typ':typ,'forms':form, 'profile':profile})
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
                return redirect('displayoffices',type_id)
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'create-office.html', {'forms': form, 'profile':profile, 'notifications': notifications, 'count': count, 'type_id':type_id})

def display_offices(request, type_id):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        office = Office.objects.filter(office_type_name_id=type_id)
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'display-offices.html', {'offices': office,'profile':profile, 'notifications': notifications, 'count': count, 'type_id': type_id})

def delete_offices(request, office_id):
    office = Office.objects.get(office_id=office_id)
    type_id = office.office_type_name_id
    office.delete()

    return redirect('displayoffices', type_id)


def edit_offices(request, office_id):
    off = Office.objects.get(office_id=office_id)

    form = OfficeForm()
  
    if request.method == 'POST':
        form = OfficeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Office.objects.filter(office_name=cd['office']):
                error = 'Office is already Created!'
            else:
                off.office_name = cd['office']
                off.save()
                return redirect('displayoffices', off.office_type_name_id)
        else:
            print(form.errors)
    user = User.objects.get(id=request.user.id)
    if MyProfile.objects.filter(profile_user_id=user.id):
        profile = MyProfile.objects.get(profile_user_id=user.id)
    else:
        profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'edit-offices.html', {'off':off, 'forms':form, 'profile':profile})
################### User Management #############################
def create_user_profile(request, user_id):
    error=' '
    
    my_user = User.objects.get(id=user_id)
    print("Office:", my_user.office)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST)

        # #to check field have no error
        # for field in prof_form:
        #     print("Field Error:", field.name,  field.errors)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            my_user.username=cd['username']
            my_user.save()
             
        else:
            print(user_form.errors)
    else:
        user_form = UpdateUserForm(instance=request.user)
       

    user = User.objects.get(id=user_id)
    if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
    else:
        profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'create-user-profile.html', {'user_form':user_form,'profile':profile,'user':user,'error':error})

def change_user_profile(request, user_id):
    
    if MyProfile.objects.filter(profile_user_id=user_id):
        profile = MyProfile.objects.get(profile_user_id=user_id)
        form = ProfileForm()
        my_user = User.objects.get(id=user_id)
        print("Profile:")
        if request.method == "POST":
            prof_form = ProfileForm(request.POST, request.FILES)
            if prof_form.is_valid():
                cd_prof = prof_form.cleaned_data
                if request.FILES and MyProfile.objects.filter(profile_user_id=my_user.id):
                    print("Image:", MyProfile.objects.filter(profile_user_id=my_user.id))
                    img=MyProfile.objects.filter(profile_user_id=my_user.id)
                    img.delete()
                else:
                    prof_form = MyProfile.objects.create(profile_user_id=my_user.id, profile_image=cd_prof['profile_image'])
                    prof_form.save()
                return redirect('signin')
            else:
               print(prof_form.errors) 
        else:
            prof_form = ProfileForm(instance=request.user)
        return render(request, 'create-user-profile.html', {'prof_form':prof_form, 'profile':profile })
    else:
        form = ProfileForm()
        my_user = User.objects.get(id=user_id)
        print("Profile:")
        if request.method == "POST":
            prof_form = ProfileForm(request.POST, request.FILES)
            if prof_form.is_valid():
                cd_prof = prof_form.cleaned_data
                prof_form = MyProfile.objects.create(profile_user_id=my_user.id, profile_image=cd_prof['profile_image'])
                prof_form.save()
                return redirect('index')
            else:
               print(prof_form.errors) 
        else:
            prof_form = ProfileForm(instance=request.user)
        return render(request, 'create-user-profile.html', {'prof_form':prof_form })

def users(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        admin = User.objects.filter(username=request.user.username)
        user = User.objects.get(id=request.user.id)
        users = User.objects.all()
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)

        return render(request, 'tables.html', {'users': users,'user':user,'profile':profile, 'notifications': notifications, 'count': count, 'admin':admin})


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
                print(off_id)
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
                
                    return redirect('user')
            else:
                error = 'Please enter valid information'
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'create-users.html', {'forms': form,'profile':profile, 'error': error, 'notifications': notifications, 'count': count})

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    
    return redirect('user')


def change_user_password(request, user_id):
    
    form = NewPasswordForm()
    error = ''
    if request.method == "POST":
        form = NewPasswordForm(request.POST)
        print("form:", form)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['password'] == cd['conf_password']:
                u = User.objects.get(id=user_id)
                 
                u.password = make_password(cd['password'])
                u.save()
                
                return redirect('user')
            else:
                error = "Password doesn't match"
        else:
            error = "Please enter valid information"
    user = User.objects.get(id=request.user.id)
    if MyProfile.objects.filter(profile_user_id=user.id):
        profile = MyProfile.objects.get(profile_user_id=user.id)
    else:
        profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'reset_password.html', {'forms': form, 'profile':profile,'error': error})

def reset_user_password(request, user_id):
    user = User.objects.get(id=user_id)
    user.username = f"{user.first_name}.{user.last_name}"
    user.password=make_password(user.username)
    messages.success('Password is Correctly Reseted!')
    user.save()
    return redirect('user')

def edit_users(request, user_id):
    
    off = Office.objects.all()
    use = User.objects.get(id=user_id)
    
    #print("User ME:", use.office.office_type_name)

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
                off_id = Office.objects.get(office_name=use.office)
                selected_office = request.POST['state']
                 
                cd = form.cleaned_data
                ty = Type.objects.get(type_name=use.office.office_type_name)

                cd['username'] = f"{cd['first_name']}.{cd['last_name']}"
                #cd['password'] = cd['username']
                # ---------------------------------------------------------------
                if User.objects.filter(username=cd['username']):
                    error = 'Username is already taken!'
                else:

                    use.first_name=cd['first_name']
                    use.last_name=cd['last_name']
                    use.username=cd['username']

                    ty.type_name=cd['type_name']
                    off_id.office_name=selected_office

                    ty.save()
                    off_id.save()
                    use.save()
                    return redirect('user')
            else:
                error = 'Please enter valid information'
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'edit-users.html', {'forms': form, 'error': error,'profile':profile, 'notifications': notifications, 'count': count})
############# Index User Dashboard###############################


def index(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        print("User:", request.user.id)
        user = User.objects.get(id=request.user.id)
        
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)

        notifications = request.user.receiver.filter(
            message_unread=True)
        count = notifications.count()
        return render(request, 'index.html', {'user': user, 'notifications': notifications, 'count': count, 'profile':profile})


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
