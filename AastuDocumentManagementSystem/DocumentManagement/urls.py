from django.conf.urls import include, url
from django.urls import path

from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('accounts/', include("django.contrib.auth.urls")),
    path('index/', views.index, name='index'),
    path('pdf/', views.pdf_rendering, name='pdf'),
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('user/', views.users, name='user'),
    path('createusers/', views.create_users, name='createusers'),
    path('createtypes/', views.create_types, name='createtypes'),
    path('displaytypes/', views.display_types, name='displaytypes'),
    path('createoffices/<int:type_id>',
         views.create_offices, name='createoffices'),
    path('displayoffices/', views.display_offices, name='displayoffices'),
    path('sendmessages/', views.send_messages, name='sendmessages'),
    # path('reset/', views.resetPassword, name='reset'),
    # path('confirmation/<str:email>/', views.confirmation, name='confirmation'),
    # path('newPassword/<str:email>/', views.newPassword, name='newPassword'),
]
