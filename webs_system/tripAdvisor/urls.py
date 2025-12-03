from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import *

app_name = 'tripAdvisor'

urlpatterns = [

    path('accounts/register/', RegisterUserView.as_view(), name='register'),

    path('listar/atracoes/', ListarAtracoes.as_view(), name='listar_atracoes'),

    path('detail/local/<int:pk>/', LocalDetailView.as_view(),name='local_detail'),

    path('detail/local/<int:pk>/', AtividadeDetailView.as_view(), name='atividade_detail'),

    path('create/atracoes/', LocalCreateView.as_view(), name='local_create'),

    path('create/atracoes/', AtividadeCreateView.as_view(), name='atividade_create'),

    path('create/', EscolherTipoAtracaoView.as_view(), name='atracao_create'),  

    path('delete/atracoes/<int:pk>/', LocalDeleteView.as_view(), name='local_delete'),  

    path('delete/atracoes/<int:pk>/', AtividadeDeleteView.as_view(), name='atividade_delete'),  

    path('update/atracoes/<int:pk>/', LocalUpdateView.as_view(), name='local_update'),

    path('update/atracoes/<int:pk>/', AtividadeUpdateView.as_view(), name='atividade_update'),
    
]