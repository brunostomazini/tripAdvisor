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
    fields = [
        'titulo', 'descricao', 'destino', 'pais_destino', 'inicio', 'final', 
        'orcamento', 'proprosito', 'notas', 'transporte'
    ]
    template_name = 'tripAdvisor/create_simple.html'
    success_url = reverse_lazy('profile')
    permission_required = 'tripAdvisor.add_viagem'
    
    def form_valid(self, form):
        form.instance.dono = self.request.user.perfil
        return super().form_valid(form)

"""class ViagemCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url=reverse_lazy('login')
    permission_required='tripAdvisor.add_viagem'

    def form_valid(self, form):
        form.instance.dono = self.request.user.perfil
        return super().form_valid(form)

    @staticmethod
    def get(request):
        form = ViagemForm()
        context = {
            'form':form
        }
        return render(request, 'tripAdvisor/create_simple.html', context)
    
    @staticmethod
    def post(request):
        form = ViagemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')
        context = {
            'form': form
        }
        return render(request, 'tripAdvisor/create_simple.html', context)
"""

    
class ViagemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Viagem
    form_class = ViagemForm 
    template_name = 'tripAdvisor/create_simple.html'
    success_url = reverse_lazy('profile') 
    permission_required = 'tripAdvisor.change_viagem'

    def get_queryset(self) -> QuerySet:
        base_qs = super().get_queryset()
        try:
            user_perfil = self.request.user.perfil
        except Perfil.DoesNotExist:
            return base_qs.none()
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

