from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import (Office,SendMessage,ReceiveMessage, Notification,Type, User)


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [ 'id','username', 'type_name']
class TypeAdmin(admin.ModelAdmin):
    fields = ['type_name']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Office)
admin.site.register(Notification)
admin.site.register(SendMessage)
admin.site.register(ReceiveMessage)
