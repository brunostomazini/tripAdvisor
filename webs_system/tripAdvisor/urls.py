from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [

    path('accounts/register/', RegisterUserView.as_view(), name='register')

]