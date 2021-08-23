from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (ConfirmationCode, Department, Document, Folder, History,
                     Media, Message, Notification, Role, User)


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Document)
admin.site.register(Department)
admin.site.register(Media)
admin.site.register(History)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Folder)
admin.site.register(ConfirmationCode)
