from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.urls import reverse_lazy
from tripAdvisor.models import Perfil
from tripAdvisor.models import Viagem
from tripAdvisor.models import Avaliacao
    

class ProfileView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):

        order_by_param = request.GET.get('order_by')
        
        valid_fields = {
            'data': '-inicio',       
            'orcamento': 'orcamento', 
            'proposito': 'proposito',  
        }
        
        
        viagens = Viagem.objects.filter(dono__user=request.user)

        if order_by_param and order_by_param in valid_fields:
            viagens = viagens.order_by(valid_fields[order_by_param])
        else:
           
            viagens = viagens.order_by('-inicio')


        try:
            perfil_do_usuario = request.user.perfil
        except Perfil.DoesNotExist:
            perfil_do_usuario = None
        avaliacoes = Avaliacao.objects.filter(perfil=perfil_do_usuario)
        context = {
            'usuario': request.user,
            'perfil': perfil_do_usuario,
            'viagens': viagens,
            'avaliacoes': avaliacoes
        }
        return render(request, 'profile.html', context)