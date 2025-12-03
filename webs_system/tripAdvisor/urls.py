from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'tripAdvisor'

urlpatterns = [

    path('accounts/register/', RegisterUserView.as_view(), name='register'),

    path('listar/atracoes/', ListarAtracoes.as_view(), name='listarAtracoes'),

    path('local/create', LocalCreateView.as_view(), name='local_create'),

    path('local/delete/<int:pk>', LocalDeleteView.as_view(), name='local_delete'),

    path('local/detail/<int:pk>', LocalDetailView.as_view(), name='local_detail'),

]