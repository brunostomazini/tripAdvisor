# Importações necessárias
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from ..models import Avaliacao
from ..forms import AvaliacaoForm

class AvaliacaoOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        avaliacao = self.get_object()

        return avaliacao.perfil.user == self.request.user or self.request.user.is_superuser

class AvaliacaoDeleteView(AvaliacaoOwnerMixin, DeleteView):
    model = Avaliacao
    template_name = 'tripAdvisor/delete.html'
    success_url = reverse_lazy('profile')


class AvaliacaoUpdateView(AvaliacaoOwnerMixin, UpdateView):
    model = Avaliacao
    form_class = AvaliacaoForm 
    template_name = 'tripAdvisor/create_simple.html'
    def get_success_url(self):
        return reverse_lazy('profile')

class AvaliacaoDetailView(DetailView):
    form_class = AvaliacaoForm
    model = Avaliacao
    template_name = 'tripAdvisor/avaliacao_detail.html'
    context_object_name = 'avaliacao' 

