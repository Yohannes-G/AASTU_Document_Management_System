from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Message, Office, Type, User,CC_User,ReceiverUser,ReplyMessage,MyProfile


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['id', 'username']


class TypeAdmin(admin.ModelAdmin):
    fields = ['type_name']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Office)
admin.site.register(Message)
admin.site.register(CC_User)
admin.site.register(ReceiverUser)
admin.site.register(ReplyMessage)
admin.site.register(MyProfile)
