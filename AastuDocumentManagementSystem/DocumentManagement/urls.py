from django.conf.urls import include, url
from django.urls import path

from django.conf.urls import include
from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('accounts/', include("django.contrib.auth.urls")),
    path('index/', views.index, name='index'),
<<<<<<< HEAD
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('doc/', views.doc, name='doc'),
=======
    path('login/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='signout'),
>>>>>>> 412892502e19a52ade9bff17c32593837b2ad86f
    path('reset/', views.resetPassword, name='reset'),
    path('confirmation/<str:email>/', views.confirmation, name='confirmation'), 
    path('newPassword/<str:email>/', views.newPassword, name='newPassword'),
]
