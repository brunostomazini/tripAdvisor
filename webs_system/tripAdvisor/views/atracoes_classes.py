from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from django.views import View 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from itertools import chain
from django.db import transaction 
from ..models import Local, Atividade 
from ..forms import *


class AtracaoCrudMixin(LoginRequiredMixin, PermissionRequiredMixin):
    login_url = reverse_lazy('login')
    template_name = 'tripAdvisor/crud_form.html' 
    def get_success_url(self):
        return reverse_lazy('tripAdvisor:listar_atracoes') 

class ListarAtracoes(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.view_atracao'
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

class LocalDetailView( DetailView):
    model = Local
    template_name = 'tripAdvisor/detail.html' 
    context_object_name = 'atracao' 

    def get_queryset(self):
        return super().get_queryset().select_related('endereco').prefetch_related(
            'categoria', 
            'avaliacoes_recebidas__perfil'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atracao = self.object
        context['model_name'] = 'local'
        context['avaliacao_form'] = AvaliacaoForm()
        context['avaliacoes'] = atracao.avaliacoes_recebidas.all().order_by('-data_avaliacao')
        context['atracao_pk'] = atracao.pk 
        
        return context

class AtividadeDetailView(DetailView):
    model = Atividade
    template_name = 'tripAdvisor/detail.html' 
    context_object_name = 'atracao'
    
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'categoria',
            'avaliacoes_recebidas__perfil' 
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        atracao = self.object 
        context['model_name'] = 'atividade'
        context['avaliacao_form'] = AvaliacaoForm()
        context['avaliacoes'] = atracao.avaliacoes_recebidas.all().order_by('-data_avaliacao')
        context['atracao_pk'] = atracao.pk
        
        return context

###Views de create
    
class EscolherTipoAtracaoView(LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'tripAdvisor/escolha.html'

class LocalCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.add_local'
    model = Local
    form_class = LocalForm
    template_name = 'tripAdvisor/atracao_form.html'
    success_url = reverse_lazy('tripAdvisor:listar_atracoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_form'] = 'Cadastrar Novo Local'
        if 'endereco_form' not in context:
            context['endereco_form'] = EnderecoForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None 
        
        local_form = self.get_form() 
        endereco_form = EnderecoForm(request.POST)

        if local_form.is_valid() and endereco_form.is_valid():
            return self.forms_valid(local_form, endereco_form)
        else:
            return self.forms_invalid(local_form, endereco_form)

    def forms_valid(self, local_form, endereco_form):

        with transaction.atomic():
            endereco_instance = endereco_form.save()
            local_instance = local_form.save(commit=False)
            local_instance.endereco = endereco_instance
            
            local_instance.save()
            local_form.save_m2m()
            
            self.object = local_instance
            return super().form_valid(local_form) 

    def forms_invalid(self, local_form, endereco_form):
        return self.render_to_response(
            self.get_context_data(form=local_form, endereco_form=endereco_form)
        )

class AtividadeCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.add_atividade'
    model = Atividade
    form_class = AtividadeForm
    template_name = 'tripAdvisor/atracao_form.html'
    success_url = reverse_lazy('tripAdvisor:listar_atracoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_form'] = 'Cadastrar Nova Atividade'
        return context


###Views de KILL 
    
class LocalDeleteView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.delete_local'
    model = Local
    template_name = 'tripAdvisor/delete.html' 
    
    success_url = reverse_lazy('tripAdvisor:listar_atracoes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_delete'] = f"Confirmar Exclusão de Local: {self.object.nome}"
        return context

class AtividadeDeleteView(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.delete_atividade'
    model = Atividade
    template_name = 'tripAdvisor/delete.html' 
    
    success_url = reverse_lazy('tripAdvisor:listar_atracoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_delete'] = f"Confirmar Exclusão de Atividade: {self.object.nome}"
        return context
    

###Views de update 
   
class LocalUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.change_local'

    model = Local
    form_class = LocalForm
    template_name = 'tripAdvisor/atracao_form.html' 
    success_url = reverse_lazy('tripAdvisor:listar_atracoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_form'] = f"Atualizar Local: {self.object.nome}"
        
        if self.request.POST:
            context['endereco_form'] = EnderecoForm(self.request.POST, instance=self.object.endereco)
        else:
            context['endereco_form'] = EnderecoForm(instance=self.object.endereco)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object() 
        local_form = self.get_form() 
        
        endereco_form = EnderecoForm(request.POST, instance=self.object.endereco)

        if local_form.is_valid() and endereco_form.is_valid():
            return self.forms_valid(local_form, endereco_form)
        else:
            return self.forms_invalid(local_form, endereco_form)

    def forms_valid(self, local_form, endereco_form):
        with transaction.atomic():
            endereco_form.save() 
            local_instance = local_form.save()
            self.object = local_instance
            return super().form_valid(local_form) 

    def forms_invalid(self, local_form, endereco_form):
        return self.render_to_response(
            self.get_context_data(form=local_form, endereco_form=endereco_form)
        )


class AtividadeUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    permission_required='tripAdvisor.change_atividade'
    model = Atividade
    form_class = AtividadeForm
    template_name = 'tripAdvisor/atracao_form.html'
    success_url = reverse_lazy('tripAdvisor:listar_atracoes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_form'] = f"Atualizar Atividade: {self.object.nome}"
        return context