from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.views import View 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from itertools import chain
from ..models import Atracao, Local, Atividade 
from ..forms import AtividadeForm, LocalForm

class AtracaoCrudMixin(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    template_name = 'tripAdvisor/crud_form.html' 
    def get_success_url(self):
        return reverse_lazy('tripAdvisor:listarAtracoes') 

class ListarAtracoes(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = reverse_lazy('login')
    permission_required = 'tripAdvisor.view_atracao'
    def get(self, request):
        locais = Local.objects.all()
        atividades = Atividade.objects.all()
        all_atracoes = sorted(
            chain(locais, atividades),
            key=lambda x: x.nome 
        )
        context = {
            'atracoes': all_atracoes
        }
        return render(request, 'tripAdvisor/list.html', context)

class LocalCreateView(AtracaoCrudMixin, CreateView):
    model = Local
    form_class = LocalForm
    permission_required = 'tripAdvisor.add_local'

class LocalUpdateView(AtracaoCrudMixin, UpdateView):
    model = Local
    form_class = LocalForm
    permission_required = 'tripAdvisor.change_local'
    
class LocalDeleteView(AtracaoCrudMixin, DeleteView):
    model = Local
    template_name = 'tripAdvisor/delete.html' 
    permission_required = 'tripAdvisor.delete_local'

class LocalDetailView(AtracaoCrudMixin, DetailView):
    model = Local
    template_name = 'tripAdvisor/detail.html'
    permission_required = 'tripAdvisor.view_local'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.model._meta.model_name 
        return context