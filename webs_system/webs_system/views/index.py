from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, TemplateView
from django.views import View 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from tripAdvisor.models import Local, Atividade
from itertools import chain 
from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q 
from itertools import chain 
import logging

class Index(TemplateView):

    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            locais = Local.objects.all().order_by('nome')
            atividades = Atividade.objects.all().order_by('turno')
            
            context['atracoes'] = list(chain(locais, atividades))
            
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            context['atracoes'] = []

        return context
    
logger = logging.getLogger(__name__)


class LocalAndAtividadeListView(TemplateView):

    template_name = 'menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query = self.request.GET.get('q')
        
        locais_qs = Local.objects.all().order_by('nome')
        atividades_qs = Atividade.objects.all().order_by('nome') 
        
        if query:

            local_filter = Q(nome__icontains=query) | Q(endereco__cidade__icontains=query)
            
            locais_qs = locais_qs.filter(local_filter)
            atividade_filter = Q(nome__icontains=query) | Q(categoria__nome__icontains=query)
            atividades_qs = atividades_qs.filter(atividade_filter)
            context['search_query'] = query

        locais = list(locais_qs)
        atividades = list(atividades_qs)

        print(f"DEBUG: Locais recuperados (após filtro): {len(locais)}") 
        print(f"DEBUG: Atividades recuperadas (após filtro): {len(atividades)}")
        
        context['atracoes'] = list(chain(locais, atividades))
        print(f"DEBUG: Total de atrações combinadas (após filtro): {len(context['atracoes'])}")

        return context