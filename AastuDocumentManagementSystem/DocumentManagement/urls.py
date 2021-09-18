from django.urls import path

from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('accounts/', include("django.contrib.auth.urls")),

    path('index/', views.index, name='index'),
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('user/', views.users, name='user'),
    path('createusers/', views.create_users, name='createusers'),
    path('userprofile/<int:user_id>/', views.create_user_profile, name='userprofile'),
    path('changeprofile/<int:user_id>/', views.change_user_profile, name='changeprofile'),
    path('deleteuser/<int:user_id>/', views.delete_user, name='deleteuser'),
    path('editusers/<int:user_id>/', views.edit_users, name='editusers'),
    path('resetpassword/<int:user_id>/', views.reset_user_password, name='resetpassword'),
    path('changepassword/<int:user_id>/', views.change_user_password, name='changepassword'),
    path('get-offices/', views.getOffices, name='get-offices'),
    path('createtypes/', views.create_types, name='createtypes'),
    path('displaytypes/', views.display_types, name='displaytypes'),
    path('deletetypes/<int:type_id>', views.delete_types, name='deletetypes'),
    path('edittypes/<int:type_id>', views.edit_types, name='edittypes'),
    path('createoffices/<int:type_id>/',views.create_offices, name='createoffices'),
    path('displayoffices/<int:type_id>/', views.display_offices, name='displayoffices'),
    path('deleteoffices/<int:office_id>/', views.delete_offices, name='deleteoffices'),
    path('editoffices/<int:office_id>/', views.edit_offices, name='editoffices'),
    path('sendmessages/', views.send_messages, name='sendmessages'),
    path('showmessage/<int:message_id>/',views.show_message, name='showmessage'),
    path('showreply/<int:reply_id>/',views.show_reply, name='showreply'),
    path('showallnotification/',views.show_all_notifications, name='showallnotification'),
    path('replymessage/<int:message_id>/',views.reply_message, name='replymessage'),
    path('showallmessage/', views.show_all_message, name='showallmessage')

]
