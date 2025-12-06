from .base_manager import BaseManager 
from ..enum import * 
from django.db.models import QuerySet
from datetime import date

class AtividadeManager(BaseManager):
    

    
    def find_by_preco(self, i: float = 100.0, f: float = 300.0) -> QuerySet['Atividade']:
        return self.filter(valor__gte=i, valor__lte=f)
    
    def find_by_categoria_duracao(self):
        return self.filter(categoria__iexact="tuor", duracao__gt=180)
    