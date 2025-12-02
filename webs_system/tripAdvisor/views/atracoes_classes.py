"""from django.views import View
from django.urls import reverse_lazy
from ..forms.atracao_form import Atracao
from ..models import Atracao
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ListarAtracoes(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url=reverse_lazy('login')
    permission_required='tripAdvisor.view_atracao'

    @staticmethod
    def get(request):
        atracoes = Atracao.objects.all()
        context = {
            'atracoes':atracoes
        }
        return render(request, 'tripAdvisor/list.html', context)"""

from django.shortcuts import render
from django.views import View 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from itertools import chain
from ..models import Atracao, Local, Atividade 

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