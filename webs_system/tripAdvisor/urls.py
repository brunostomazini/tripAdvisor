from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import RegisterUserView
from .views import ListarAtracoes

urlpatterns = [

    path('accounts/register/', RegisterUserView.as_view(), name='register'),

    path('listar/atracoes/', ListarAtracoes.as_view(), name='listarAtracoes'),

]