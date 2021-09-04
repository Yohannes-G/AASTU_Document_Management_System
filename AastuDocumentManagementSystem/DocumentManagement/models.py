from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
<<<<<<< HEAD
class User(AbstractUser):
    type_name = models.CharField(max_length=50)
    office = models.CharField(max_length=50)

    #is_active = models.BooleanField(default=True)
    # staff = models.BooleanField(default=False) # a admin user; non super-user
    # admin = models.BooleanField(default=False) # a superuser
    def __str__(self):
        return self.first_name


=======
>>>>>>> 9723e0191e65e74b324798e7bdbc65858dda87ac
class Type(models.Model):
    type_id = models.BigAutoField(primary_key=True)
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

<<<<<<< HEAD
=======

>>>>>>> 9723e0191e65e74b324798e7bdbc65858dda87ac
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


class Message(models.Model):
    message_time = models.DateTimeField(auto_now_add=True)
    message_id = models.BigAutoField(primary_key=True)
    # message_cc = models.BooleanField(max_length=50)
    message_unread = models.BooleanField(default=True)
    message_description = models.TextField(max_length=256)
    message_file = models.FileField(
        blank=True)
    message_receiver = models.ManyToManyField(User, related_name='receiver')
    message_sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
