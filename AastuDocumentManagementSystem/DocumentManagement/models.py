from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class User(AbstractUser):
    type_name = models.CharField(max_length=50)
    office = models.CharField(max_length=50)

    #is_active = models.BooleanField(default=True)
    # staff = models.BooleanField(default=False) # a admin user; non super-user
    # admin = models.BooleanField(default=False) # a superuser
    def __str__(self):
        return self.first_name


class Type(models.Model):
    type_id = models.BigAutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    def __str__(self):
        return self.type_name

class Office(models.Model):
    office_id = models.BigAutoField(primary_key=True)
    office_name = models.CharField(max_length=50)
    office_type_name = models.ForeignKey(Type, on_delete=models.CASCADE)
    def __str__(self):
        return self.office_name
 

  
class Notification(models.Model):
    notify_id = models.BigAutoField(primary_key=True)
    notify_date = models.DateField()

class SendMessage(models.Model):
    message_id = models.BigAutoField(primary_key=True)
    message_type_name = models.CharField(max_length=50)
    message_office = models.CharField(max_length=50)
    message_cc_type_name = models.CharField(max_length=50)
    message_cc_office = models.CharField(max_length=50) 
    message_description = models.TextField(max_length=256)
    message_file = models.FileField(blank=True)
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE)

class ReceiveMessage(models.Model):
    message_id = models.BigAutoField(primary_key=True)
    message_name = models.CharField(max_length=50)
    message_content = models.TextField(max_length=256)
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE)
