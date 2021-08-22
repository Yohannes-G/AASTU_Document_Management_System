from django.urls import path

# from django.conf.urls import include
from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('reset/', views.resetPassword, name='reset'),
    path('confirmation/<str:email>/', views.confirmation, name='confirmation'),
    path('newPassword/<str:email>/', views.newPassword, name='newPassword'),
]
