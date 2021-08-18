from django.urls import path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import include
from .views import UserViewSet
from . import views

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
	path('',views.index, name='index'),
	path('', include(router.urls))
]