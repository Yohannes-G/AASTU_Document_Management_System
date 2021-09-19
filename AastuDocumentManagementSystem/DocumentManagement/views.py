import os
from itertools import chain
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
from django.contrib import auth
from django.contrib import messages as toast_msgs
from django.contrib.auth.hashers import make_password
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render

from .forms import (MessageFilterForm, NewPasswordForm, NotificationFilterForm,
                    OfficeForm, ProfileForm, ReplyMessageForm, SendMessageForm,
                    SignInForm, SignUPForm, TypeForm, UpdateUserForm)
from .models import (CC_User, Message, MyProfile, Office, ReceiverUser,
                     ReplyMessage, Type, User)

######################## Drop Down ##############################


########################### Get All Message #####################
def detailed_messages(messages):
    lst = []
    for message in messages:
        try:
            for receiver in message.receiver.all():
                lst.append(receiver)
        except:
            pass
        try:
            for receiver in message.reply_receiver.all():
                lst.append(receiver)
        except:
            pass
        try:
            for receiver in message.message_cc.all():
                lst.append(receiver)
        except:
            pass
        try:
            for receiver in message.reply_cc.all():
                lst.append(receiver)
        except:
            pass
    return lst


########################### Get Message notification #############

def message_notification(request):
    notifications = detailed_messages(
        request.user.cc_user.filter(unread=True))
    messages = detailed_messages(
        request.user.receiver_user.filter(unread=True))
    user = User.objects.get(id=request.user.id)
    if MyProfile.objects.filter(profile_user_id=user.id):
        profile = MyProfile.objects.get(profile_user_id=user.id)
    else:
        profile = MyProfile.objects.filter(profile_user_id=user.id)
    return {'notifications': notifications, 'messages': messages, 'profile': profile}

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
        msg_ntf = message_notification(request)
        notifications = msg_ntf['notifications']
        messages = msg_ntf['messages']
        if request.method == 'POST':
            form = SendMessageForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                category = request.FILES['file'].content_type.split(
                    '/')[-1].capitalize()
                selected_cc_office = request.POST['cc_state']
                selected_office = request.POST['state']
                users = User.objects.filter(
                    office__office_name=selected_office)
                receivers = []
                for user in users:
                    receiver = ReceiverUser.objects.create(user=user)
                    receiver.save()
                    receivers.append(receiver)
                carbon_copies = User.objects.filter(
                    office__office_name=selected_cc_office)
                cc_users = []
                for carbon_copy in carbon_copies:
                    receiver = CC_User.objects.create(user=carbon_copy)
                    receiver.save()
                    cc_users.append(receiver)

                send = Message(
                    message_description=cd['description'],
                    message_file=request.FILES['file'],
                    message_sender=request.user,
                )
                send.message_file.field.upload_to = f"{request.user.office}/{request.user.username}/{category}"
                send.save()
                send.message_receiver.add(*receivers)
                send.message_cc.add(*cc_users)
                return redirect('showallmessage')
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'create-send-message.html',
                      {'forms': form, 'notifications': notifications, 'profile': profile, 'messages': messages, 'user': user})

################### Reply Message for received message #############


def reply_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        msg_ntf = message_notification(request)
        notifications = msg_ntf['notifications']
        messages = msg_ntf['messages']
        msg = Message.objects.get(message_id=message_id)
        office = msg.message_sender.office
        type_name = msg.message_sender.office.office_type_name
        form = ReplyMessageForm()
        if request.method == 'POST':
            form = ReplyMessageForm(request.POST, request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                category = request.FILES['file'].content_type.split(
                    '/')[-1].capitalize()
                selected_cc_office = request.POST['cc_state']
                users = User.objects.filter(
                    office__office_name=office)
                receivers = []
                for user in users:
                    receiver = ReceiverUser.objects.create(user=user)
                    receiver.save()
                    receivers.append(receiver)
                carbon_copies = User.objects.filter(
                    office__office_name=selected_cc_office)
                cc_users = []
                for carbon_copy in carbon_copies:
                    receiver = CC_User.objects.create(user=carbon_copy)
                    receiver.save()
                    cc_users.append(receiver)

                send = ReplyMessage(
                    reply_description=cd['description'],
                    reply_file=request.FILES['file'],
                    reply_sender=request.user,
                    replyed_message=msg
                )
                send.reply_file.field.upload_to = f"{request.user.office}/{request.user.username}/{category}"
                send.save()
                send.reply_receiver.add(*receivers)
                send.reply_cc.add(*cc_users)
                return redirect('showallmessage')
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'create-send-message.html',
                      {'forms': form, 'type_name': type_name, 'office': office, 'notifications': notifications, 'messages': messages, 'profile': profile})

################## Show Message ############################


def show_message(request, message_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        msg = Message.objects.get(message_id=message_id)
        try:
            unread = msg.message_receiver.get(user=request.user)
            unread.unread = False
            unread.save()
        except:
            unread = msg.message_cc.get(user=request.user)
            unread.unread = False
            unread.save()
        msg_ntf = message_notification(request)
        notifications = msg_ntf['notifications']
        messages = msg_ntf['messages']
        carbon_copy = bool(msg.message_cc.filter(user=request.user))

        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'show_message.html', {'msg': msg, 'notifications': notifications, 'messages': messages, 'carbon_copy': carbon_copy, 'profile': profile})


################## Show Reply ############################
def show_reply(request, reply_id):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        msg = ReplyMessage.objects.get(reply_id=reply_id)
        try:
            unread = msg.reply_receiver.get(user=request.user)
            unread.unread = False
            unread.save()
        except:
            unread = msg.reply_cc.get(user=request.user)
            unread.unread = False
            unread.save()
        msg_ntf = message_notification(request)
        notifications = msg_ntf['notifications']
        messages = msg_ntf['messages']
        carbon_copy = bool(msg.reply_cc.filter(user=request.user))
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'show_reply.html', {'msg': msg, 'notifications': notifications, 'profile': profile, 'messages': messages, 'carbon_copy': carbon_copy})


################### Show all messages ########################


def send_message(request):
    send_messages = list(request.user.sender.all())
    reply_send_messages = list(request.user.reply_sender.all())
    return list(chain(send_messages, reply_send_messages))


def filter_message_type_receiver(receive_msgs, selected_type):
    receive_msg = []
    for msg in receive_msgs:
        try:
            if msg.message_sender.office.office_type_name.type_name == selected_type:
                receive_msg.append(msg)
        except:
            if msg.reply_sender.office.office_type_name.type_name == selected_type:
                receive_msg.append(msg)
    return receive_msg


def filter_message_office_receiver(receive_msgs, selected_office):
    receive_msg = []
    for msg in receive_msgs:
        try:
            if msg.message_sender.office.office_name == selected_office:
                receive_msg.append(msg)
        except:
            if msg.reply_sender.office.office_name == selected_office:
                receive_msg.append(msg)
    return receive_msg


def filter_message_type_sender(send_msgs, selected_type):
    send_msg = []
    for msg in send_msgs:
        try:
            for receiver in msg.message_receiver.all():
                if receiver.user.office.office_type_name.type_name == selected_type:
                    send_msg.append(msg)
        except:
            for receiver in msg.reply_receiver.all():
                if receiver.user.office.office_type_name.type_name == selected_type:
                    send_msg.append(msg)
    return send_msg


def filter_message_office_sender(send_msgs, selected_office):
    send_msg = []
    for msg in send_msgs:
        try:
            for receiver in msg.message_receiver.all():
                if receiver.user.office.office_name == selected_office:
                    send_msg.append(msg)
        except:
            for receiver in msg.reply_receiver.all():
                if receiver.user.office.office_name == selected_office:
                    send_msg.append(msg)
    return send_msg


def filter_notification_office(all_msgs, sender_office, receiver_office=False, send=True):
    all_msg = []
    if not send:
        all_msg.extend(filter_message_office_sender(all_msgs, sender_office))

        if receiver_office:
            all_msg = filter_message_office_receiver(all_msg, receiver_office)
    else:
        all_msg.extend(
            filter_message_office_receiver(all_msgs, sender_office))
        if receiver_office:
            all_msg = filter_message_office_sender(
                all_msg, receiver_office)
    return all_msg


def filter_notification_type(all_msgs, sender_type, receiver_type=False, send=True):
    all_msg = []
    if not send:
        all_msg.extend(
            filter_message_type_sender(all_msgs, sender_type))
        if receiver_type:
            all_msg = filter_message_type_receiver(all_msg, receiver_type)
    else:
        all_msg.extend(filter_message_type_receiver(all_msgs, sender_type))
        if receiver_type:
            all_msg = filter_message_type_sender(all_msg, receiver_type)
    return all_msg


def show_all_message(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        receive_msgs = request.user.receiver_user.all()
        receive_msgs = list(detailed_messages(receive_msgs))
        send_msgs = send_message(request)
        user = request.user
        all_messages = list(chain(send_msgs, receive_msgs))
        msg_ntf = message_notification(request)
        notifications = msg_ntf['notifications']
        messages = msg_ntf['messages']
        form = MessageFilterForm()
        form.fields['type_name'].choices = get_type()
        if request.method == "POST":
            form = MessageFilterForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                selected_office = request.POST['state']
                if cd['type_name'] != "All":
                    if selected_office != "All":
                        if (cd['action'] == "1" or cd['action'] == "0"):
                            if cd['action'] == "1":
                                send_msgs = []
                            receive_msgs = filter_message_office_receiver(
                                receive_msgs, selected_office)
                        if (cd['action'] == "0" or cd['action'] == "2"):
                            if cd['action'] == "2":
                                receive_msgs = []
                            send_msgs = filter_message_office_sender(
                                send_msgs, selected_office)
                    else:
                        if (cd['action'] == "1" or cd['action'] == "0"):
                            if cd['action'] == "1":
                                send_msgs = []
                            receive_msgs = filter_message_type_receiver(
                                receive_msgs, cd['type_name'])
                        if (cd['action'] == "2" or cd['action'] == "0"):
                            if cd['action'] == "2":
                                receive_msgs = []
                            send_msgs = filter_message_type_sender(
                                send_msgs, cd['type_name'])
                else:
                    if cd['action'] == "1":
                        send_msgs = []
                    elif cd['action'] == "2":
                        receive_msgs = []
                all_messages = list(chain(send_msgs, receive_msgs))
        u = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=u.id):
            profile = MyProfile.objects.get(profile_user_id=u.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'show_all_message.html', {'all_messages': all_messages, 'user': user,
                                                     'notifications': notifications, 'messages': messages, 'profile': profile,
                                                     'form': form
                                                     })


def show_all_notifications(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        all_messages = detailed_messages(request.user.cc_user.all())
        user = request.user
        msg_ntf = message_notification(request)
        notifications = msg_ntf['notifications']
        messages = msg_ntf['messages']
        form = NotificationFilterForm()
        if request.method == "POST":
            form = NotificationFilterForm(request.POST)
            if form.is_valid():
                print("form validation")
                cd = form.cleaned_data
                selected_office = request.POST['state']
                selected_to_office = request.POST['to_state']
                all_msgs = []
                if cd['type_name'] != "All":
                    if selected_office != "All":
                        if cd['to_type_name'] != "All":
                            if selected_to_office != "All":
                                if (cd['action'] == "1" or cd['action'] == "0"):
                                    all_msgs.extend(filter_notification_office(
                                        all_messages, selected_office, selected_to_office, False))
                                    print("Type of type")
                                    print(all_msgs)
                                if (cd["action"] == "2" or cd["action"] == "0"):
                                    all_msgs.extend(filter_notification_office(
                                        all_messages, selected_office, selected_to_office))
                                    print("Office of office")
                            else:
                                if (cd['action'] == "1" or cd['action'] == "0"):
                                    all_msgs.extend(filter_notification_office(
                                        all_messages, selected_office, send=False))
                                    all_msgs.extend(filter_notification_type(
                                        all_msgs, cd['type_name'], cd['to_type_name'], False))
                                if (cd['action'] == "2" or cd['action'] == "0"):
                                    all_msgs.extend(filter_notification_office(
                                        all_messages, selected_office))
                                    all_msgs.extend(filter_notification_type(
                                        all_msgs, cd['type_name'], cd['to_type_name']))
                        else:
                            if (cd['action'] == "1" or cd['action'] == "0"):
                                all_msgs.extend(filter_notification_office(
                                    all_messages, selected_office, send=False))
                            if (cd['action'] == "2" or cd['action'] == "0"):
                                all_msgs.extend(filter_notification_office(
                                    all_messages, selected_office))
                    else:
                        if cd['to_type_name'] != "All":
                            if selected_to_office != "All":
                                if (cd['action'] == "1" or cd['action'] == "0"):
                                    all_msgs.extend(filter_notification_office(
                                        all_messages, selected_to_office))
                                    all_msgs.extend(filter_notification_type(
                                        all_msgs, cd['type_name'], cd['to_type_name'], False))
                                if (cd["action"] == "2" or cd["action"] == "0"):
                                    all_msgs.extend(filter_notification_office(
                                        all_messages, selected_to_office, send=False))
                                    all_msgs.extend(filter_notification_type(
                                        all_msgs, cd['type_name'], cd['to_type_name']))
                            else:
                                if (cd['action'] == "1" or cd['action'] == "0"):
                                    all_msgs.extend(filter_notification_type(
                                        all_messages, cd['type_name'], cd['to_type_name'], False))
                                if (cd['action'] == "2" or cd['action'] == "0"):
                                    all_msgs.extend(filter_notification_type(
                                        all_messages, cd['type_name'], cd['to_type_name']))
                        else:
                            if (cd['action'] == "1" or cd['action'] == "0"):
                                all_msgs.extend(filter_notification_type(
                                    all_messages, cd['type_name'], send=False))
                            if (cd['action'] == "2" or cd['action'] == "0"):
                                all_msgs.extend(filter_notification_type(
                                    all_messages, cd['type_name']))
                else:
                    all_msgs = all_messages
                all_messages = all_msgs
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'show_all_notifications.htm', {'all_messages': all_messages, 'messages': messages, 'user': user, 'profile': profile, 'notifications': notifications, 'form': form})


################### Create Roles #############################
def create_types(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        error = ""
        form = TypeForm()
        if request.method == 'POST':
            form = TypeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    Type.objects.get(type_name=cd['type_name'])
                except:
                    role = Type.objects.create(type_name=cd['type_name'])
                    role.save()
                    redirect('displytypes')
                error = f"{cd['type_name']} is already registered"
    user = User.objects.get(id=request.user.id)
    if MyProfile.objects.filter(profile_user_id=user.id):
        profile = MyProfile.objects.get(profile_user_id=user.id)
    else:
        profile = MyProfile.objects.filter(profile_user_id=user.id)
    return render(request, 'create-role.html', {'forms': form, 'profile': profile, 'error': error})


def display_types(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        types = Type.objects.all()
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'display-types.html', {'types': types, 'profile': profile})


def delete_types(request, type_id):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        typ = Type.objects.get(type_id=type_id)
        typ.delete()
        #messages.error(request, 'Type deleted.')
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
    return render(request, 'edit-types.html', {'typ': typ, 'forms': form, 'profile': profile})
################### Create Offices #############################


def create_offices(request, type_id):

    if not request.user.is_staff:
        return redirect('signin')
    else:
        error = ""
        messages = ""
        notifications = ""
        # message_notification = request.user.receiver.filter(
        #     message_unread=True)
        # notifications = message_notification.filter(message_cc=True)
        # messages = message_notification.filter(message_cc=False)
        form = OfficeForm()
        type_name = Type.objects.get(type_id=type_id)
        if request.method == 'POST':
            form = OfficeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    Office.objects.get(
                        office_name=cd['office'])
                except:
                    office = Office.objects.create(
                        office_type_name_id=type_id, office_name=cd['office'])
                    office.save()
                    redirect('displayoffices', type_id=type_id)
                error = f"{cd['office']} is already registered"
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'create-office.html', {'forms': form, 'profile': profile, 'type_id': type_id, 'error': error, 'type_name': type_name})

        # return render(request, 'create-office.html', {
        #     # 'forms': form, 'notifications': notifications,
        #     # 'messages': messages,
        #     'type_name': type_name})


def display_offices(request, type_id):
    if not request.user.is_staff:
        return redirect('signin')
    else:
        type_name = Type.objects.get(type_id=type_id)
        office = Office.objects.filter(office_type_name_id=type_id)
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)
        return render(request, 'display-offices.html', {'offices': office, 'profile': profile, 'type_id': type_id, 'type_name': type_name})


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
    return render(request, 'edit-offices.html', {'off': off, 'forms': form, 'profile': profile})
################### User Management #############################


def create_user_profile(request, user_id):
    error = ' '

    my_user = User.objects.get(id=user_id)
    print("Office:", my_user.office)
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST)

        # #to check field have no error
        # for field in prof_form:
        #     print("Field Error:", field.name,  field.errors)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            my_user.username = cd['username']
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
    return render(request, 'create-user-profile.html', {'user_form': user_form, 'profile': profile, 'user': user, 'error': error})


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
                    print("Image:", MyProfile.objects.filter(
                        profile_user_id=my_user.id))
                    img = MyProfile.objects.filter(profile_user_id=my_user.id)
                    img.delete()
                else:
                    prof_form = MyProfile.objects.create(
                        profile_user_id=my_user.id, profile_image=cd_prof['profile_image'])
                    prof_form.save()
                return redirect('signin')
            else:
                print(prof_form.errors)
        else:
            prof_form = ProfileForm(instance=request.user)
        return render(request, 'create-user-profile.html', {'prof_form': prof_form, 'profile': profile})
    else:
        form = ProfileForm()
        my_user = User.objects.get(id=user_id)
        print("Profile:")
        if request.method == "POST":
            prof_form = ProfileForm(request.POST, request.FILES)
            if prof_form.is_valid():
                cd_prof = prof_form.cleaned_data
                prof_form = MyProfile.objects.create(
                    profile_user_id=my_user.id, profile_image=cd_prof['profile_image'])
                prof_form.save()
                return redirect('index')
            else:
                print(prof_form.errors)
        else:
            prof_form = ProfileForm(instance=request.user)
        return render(request, 'create-user-profile.html', {'prof_form': prof_form})


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
    print("return:", typeId)

    for x in all_data:
        print(x)
        if x == type_name:
            office_list = Office.objects.filter(
                office_type_name_id=typeId.type_id)
            print("office_list", office_list)
            for office in office_list:
                print("Office New:", office)
                y = (office, office)
                all_offices.append(office)
                print("all_offices", all_offices)
    return all_offices


def getOffices(request):
    office_type_name = request.POST.get('type_name')
    office_name = request.POST.get('office_name')
    print("officename", office_name)
    #office_type_name = 'Director'
    print("getOffices: ", office_type_name)
    offices = return_office_by_type(office_type_name)
    office = [
        office.office_name for office in offices if office.office_name != office_name and request.user.office != office]

    return JsonResponse(office,  safe=False)


def users(request):
    if not request.user.is_staff:
        return redirect('signin')
    else:

        admin = User.objects.filter(username=request.user.username)
        user = User.objects.get(id=request.user.id)
        users = User.objects.all()
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)

        return render(request, 'tables.html', {'users': users, 'user': user, 'profile': profile, 'admin': admin})


def create_users(request):
    ty = Type.objects.all()
    off = Office.objects.all()
    user = User.objects.all()

    if not request.user.is_staff:
        return redirect('signin')
    else:
        error = ""

        form = SignUPForm()
        if request.method == "POST":
            form = SignUPForm(request.POST)
            if form.is_valid():

                # --------------------------------------------------------------
                off_id = Office.objects.get(office_name=request.POST['state'])
                print(off_id)
                selected_office = request.POST['state']

                cd = form.cleaned_data
                print(cd)
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
        return render(request, 'create-users.html', {'forms': form, 'profile': profile, 'error': error})


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
    return render(request, 'reset_password.html', {'forms': form, 'profile': profile, 'error': error})


def reset_user_password(request, user_id):
    user = User.objects.get(id=user_id)
    user.username = f"{user.first_name}.{user.last_name}"
    user.password = make_password(user.username)
    # messages.success('Password is Correctly Reseted!')
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
                # --------------------------------------------------------------
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

                    use.first_name = cd['first_name']
                    use.last_name = cd['last_name']
                    use.username = cd['username']

                    ty.type_name = cd['type_name']
                    off_id.office_name = selected_office

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
        return render(request, 'edit-users.html', {'forms': form, 'error': error, 'profile': profile})
############# Index User Dashboard###############################


def index(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    else:
        url = "http://www.aastu.edu.et/category/newsevents/"
        page = requests.get(url)
        text = page.content
        soup = BeautifulSoup(text, 'html.parser')
        with open('templates/news.html', 'w', encoding='utf-8') as aastu:
            aastu.write(str(soup.prettify()))
        user = User.objects.get(id=request.user.id)
        if MyProfile.objects.filter(profile_user_id=user.id):
            profile = MyProfile.objects.get(profile_user_id=user.id)
        else:
            profile = MyProfile.objects.filter(profile_user_id=user.id)

        msg_ntf = message_notification(request)
        notifications = msg_ntf['notifications']
        messages = msg_ntf['messages']
        return render(request, 'index.html', {'user': user, 'notifications': notifications, 'messages': messages, 'profile': profile})


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
                toast_msgs.success(
                    request, f"You are now logged in as {cd['username']}.")
                # messages.info(
                #     request, f"You are now logged in as {cd['username']}.")
                return redirect('index')
            else:
                error = 'Username or password is incorrect!'
        else:
            error = 'Please enter valid information'
    return render(request, 'sign-in.html', {'forms': form, 'error': error})


def signout(request):
    auth.logout(request)
    # messages.info(request, f"You are now logged out.")
    if not request.user.is_authenticated:
        return redirect('signin')
