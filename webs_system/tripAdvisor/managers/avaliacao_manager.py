from .base_manager import BaseManager
from datetime import date
from ..enum import * 
from django.db.models import QuerySet
from ..models import Local



class AvaliacaoManager(BaseManager):

    def find_avaliacoes_atuais(self) -> list["Avaliacao"]:
        ano_atual = date.today().year
        return self.filter(data_avaliacao__year=ano_atual)
    
    def find_melhores_portugues(self) -> QuerySet['Avaliacao']:
        return self.filter(likes__gte=5, perfil__lingua__iexact="Português")
    
    def find_uteis_by_local(self, local: 'Local') -> QuerySet:
        return self.filter(atracao=local,likes__gte=10)