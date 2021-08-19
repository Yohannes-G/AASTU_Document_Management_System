from django.urls import path

from . import views

urlpatterns = [
    path('signIn/', views.signIn)
]
