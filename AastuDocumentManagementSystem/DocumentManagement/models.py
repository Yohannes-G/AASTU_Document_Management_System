from django.contrib.auth.models import AbstractUser
from django.db import models


class Type(models.Model):
    type_id = models.BigAutoField(primary_key=True)
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Office(models.Model):
    office_id = models.BigAutoField(primary_key=True)
    office_name = models.CharField(max_length=50)
    office_type_name = models.ForeignKey(
        Type, on_delete=models.CASCADE, related_name='office_type')

    def __str__(self):
        return self.office_name


class User(AbstractUser):
    office = models.ForeignKey(
        Office, on_delete=models.CASCADE, related_name='office')

    def __str__(self):
        return self.first_name


class CC_User(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cc_user')
    unread = models.BooleanField(default=True)


class ReceiverUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver_user')
    unread = models.BooleanField(default=True)


class Message(models.Model):
    message_time = models.DateTimeField(auto_now_add=True)
    message_id = models.BigAutoField(primary_key=True)
    message_cc = models.ManyToManyField(CC_User, related_name='message_cc')
    message_description = models.TextField(max_length=256)
    message_file = models.FileField(
        blank=True)
    message_sender = models.ForeignKey(
        User, related_name='sender', on_delete=models.CASCADE)
    message_receiver = models.ManyToManyField(
        ReceiverUser, related_name='receiver')


class ReplyMessage(models.Model):
    reply_time = models.DateTimeField(auto_now_add=True)
    reply_id = models.BigAutoField(primary_key=True)
    reply_cc = models.ManyToManyField(CC_User, related_name='reply_cc')
    reply_description = models.TextField(max_length=256)
    reply_file = models.FileField(
        blank=True)
    reply_sender = models.ForeignKey(
        User, related_name='reply_sender', on_delete=models.CASCADE)
    reply_receiver = models.ManyToManyField(
        ReceiverUser, related_name='reply_receiver')
    replyed_message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='replyed_message')

class MyProfile(models.Model):
    prof_id = models.BigAutoField(primary_key=True)
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/', default='Space3.jpg')