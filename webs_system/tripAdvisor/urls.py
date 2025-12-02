from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import RegisterUserView

urlpatterns = [

    path('accounts/register/', RegisterUserView.as_view(), name='register')

]