from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_first_name = models.CharField(max_length=50)
    user_last_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_password = models.CharField(max_length=50)
    user_confirm_password = models.CharField(max_length=50)
    user_sex = models.CharField(max_length=10)


class Role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=50)
    role_description = models.TextField(max_length=256)


class Document(models.Model):
    doc_id = models.BigAutoField(primary_key=True)
    doc_name = models.CharField(max_length=50)
    doc_content = models.FileField(blank=True)


class Department(models.Model):
    dept_id = models.BigAutoField(primary_key=True)
    dept_name = models.CharField(max_length=50)
    dept_course_name = models.CharField(max_length=50)
    dept_cours_id = models.IntegerField()


class Media(models.Model):
    media_id = models.BigAutoField(primary_key=True)
    media_name = models.CharField(max_length=50)
    media_content = models.FileField(blank=True)


class History(models.Model):
    history_id = models.BigAutoField(primary_key=True)
    history_date = models.DateField()


class Notification(models.Model):
    notify_id = models.BigAutoField(primary_key=True)
    notify_date = models.DateField()


class Message(models.Model):
    message_id = models.BigAutoField(primary_key=True)
    message_name = models.CharField(max_length=50)
    message_content = models.TextField(max_length=256)


class Folder(models.Model):
    folder_id = models.BigAutoField(primary_key=True)
    folder_name = models.CharField(max_length=50)
