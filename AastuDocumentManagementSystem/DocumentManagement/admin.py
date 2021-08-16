from django.contrib import admin
from .models import User,Role,Document,Department,Media,History,Notification,Message,Folder
# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Document)
admin.site.register(Department)
admin.site.register(Media)
admin.site.register(History)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Folder)
