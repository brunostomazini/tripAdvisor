# Importações necessárias
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from ..models import Avaliacao, Atracao, Perfil
from ..forms import AvaliacaoForm

class AvaliacaoOwnerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        avaliacao = self.get_object()

        return avaliacao.perfil.user == self.request.user or self.request.user.is_superuser

class AvaliacaoDeleteView(AvaliacaoOwnerMixin, DeleteView):
    model = Avaliacao
    template_name = 'tripAdvisor/delete.html'
    success_url = reverse_lazy('profile')


class AvaliacaoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'tripAdvisor/create_simple.html' 
    success_url = reverse_lazy('tripAdvisor:perfil') 
    permission_required = 'tripAdvisor.add_avaliacao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_model_name'] = 'avaliacao' 
        return context
    
    def form_valid(self, form):
        form.instance.dono = self.request.user.perfil
        return super().form_valid(form)

class AvaliacaoDetailView(DetailView):
    form_class = AvaliacaoForm
    model = Avaliacao
    template_name = 'tripAdvisor/avaliacao_detail.html'
    context_object_name = 'avaliacao' 

class AvaliacaoCreateView(LoginRequiredMixin, CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'tripAdvisor/create_simple.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atracao_pk'] = self.kwargs['pk'] 
        return context
    
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def form_valid(self, form):
        try:
            perfil = self.request.user.perfil
            form.instance.perfil = perfil
        except Perfil.DoesNotExist:
            form.add_error(None, "Perfil do usuário logado não encontrado.")
            return self.form_invalid(form)
        
        atracao_pk = self.kwargs.get('pk')
        
        try:
            atracao = get_object_or_404(Atracao, pk=atracao_pk)
            form.instance.atracao = atracao
        except Atracao.DoesNotExist:
            form.add_error(None, f"Atração com ID {atracao_pk} não encontrada.")
            return self.form_invalid(form)
        if Avaliacao.objects.filter(perfil=perfil, atracao=atracao).exists():
            form.add_error(None, "Você já possui uma avaliação registrada para esta atração. Por favor, edite a avaliação existente.")
            return self.form_invalid(form)
        
        return super().form_valid(form)