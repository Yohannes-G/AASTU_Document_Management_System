from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class User(AbstractUser):
    sex = models.CharField(max_length=10)
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


class Role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=50)
    role_description = models.TextField(max_length=256)


class Document(models.Model):
    department_choice = (
        ('Colledge', ('Colledge')),
        ('Directories', ('Directories')),
        ('COE', ('COE'))
    )
    doc_id = models.BigAutoField(primary_key=True)
    doc_title = models.CharField(max_length=50)
    doc_desc = models.TextField(max_length=300)
    doc_file = models.FileField(blank=True, upload_to='documents/')
    doc_department = models.CharField(
        max_length=20, choices=department_choice, default='Colledge')
    doc_sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Sender")
    doc_receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="Receiver")
    doc_date = models.DateTimeField(auto_now_add=True)


class Department(models.Model):
    dept_id = models.BigAutoField(primary_key=True)
    dept_name = models.CharField(max_length=50)
    dept_course_name = models.CharField(max_length=50)
    dept_course_id = models.IntegerField()


class Media(models.Model):
    media_id = models.BigAutoField(primary_key=True)
    media_name = models.CharField(max_length=50)
    media_content = models.FileField(blank=True)


class History(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    history_date = models.DateField()


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
