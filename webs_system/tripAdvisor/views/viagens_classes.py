from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from django.views import View 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ..models import *
from ..forms import *
from django.db.models import QuerySet

class ViagemDetailView(LoginRequiredMixin, PermissionRequiredMixin,DetailView):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.view_viagem'
    model = Viagem
    template_name = 'tripAdvisor/viagem_detail.html' 

class ViagemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Viagem
    # Usando 'fields' conforme seu código, ou 'form_class = ViagemForm' se preferir usar o Form
    form_class = ViagemForm
    template_name = 'tripAdvisor/create_simple.html' 
    success_url = reverse_lazy('profile') 
    permission_required = 'tripAdvisor.add_viagem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # CRUCIAL: Injeta o nome do modelo
        context['form_model_name'] = 'viagem' 
        return context
    
    def form_valid(self, form):
        form.instance.dono = self.request.user.perfil
        return super().form_valid(form)

# View de Atualização de Viagem (ADICIONADO get_context_data)
class ViagemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Viagem
    form_class = ViagemForm 
    template_name = 'tripAdvisor/create_simple.html'
    success_url = reverse_lazy('profile') # Corrigido namespace aqui também
    permission_required = 'tripAdvisor.change_viagem'

    # ADICIONADO: Método para injetar o contexto necessário para o template genérico
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # CRUCIAL: Injeta o nome do modelo
        context['form_model_name'] = 'viagem' 
        return context
    
    def get_queryset(self) -> QuerySet:
        base_qs = super().get_queryset()
        try:
            # Assumindo que Perfil está acessível via request.user
            user_perfil = self.request.user.perfil
        except Perfil.DoesNotExist:
            # Retorna um queryset vazio se o perfil não existir
            return base_qs.none()
        # Filtra para que apenas o dono possa atualizar
        return base_qs.filter(dono=user_perfil)
    
class ViagemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Viagem
    template_name = 'tripAdvisor/delete.html' 
    success_url = reverse_lazy('profile') 
    permission_required = 'tripAdvisor.delete_viagem'
    context_object_name = 'viagem'

    def get_queryset(self) -> QuerySet:

        base_qs = super().get_queryset()
        try:
            user_perfil = self.request.user.perfil
        except Perfil.DoesNotExist:
            return base_qs.none()
            
        return base_qs.filter(dono=user_perfil)

