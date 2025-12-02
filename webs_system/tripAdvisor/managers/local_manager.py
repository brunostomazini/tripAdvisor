from .base_manager import BaseManager
from django.db.models import QuerySet
from ..enum import *

class LocalManager(BaseManager):
    
    def find_by_cidade(self, cidade: str) -> QuerySet:
        return self.filter(endereco__cidade__icontains=cidade)
    
    def find_by_nota_minima(self) -> QuerySet:
        return self.filter(nota__gte=4.5, nota__isnull=False)
    
    def find_by_no_endereco(self) -> QuerySet:
        return self.filter(endereco__isnull=True)
    
    def find_by_pais(self, lista: list) -> list['Local']:
        locais = self.filter(endereco__pais__in=lista)
        return list(locais)
    
    def find_by_site_br(self) -> QuerySet:
        return self.filter(site__iendswith="br")
    
    

    #def find_by

    #def find_by