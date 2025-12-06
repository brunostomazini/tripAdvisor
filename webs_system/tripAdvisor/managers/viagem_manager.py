from .base_manager import BaseManager 
from ..enum import * 
from django.db.models import QuerySet
from ..models import Perfil

class ViagemManager(BaseManager):
    
    def find_by_user(self, user) -> QuerySet['Perfil']:
        if not user.is_authenticated:
            return self.none()     
        try:
            perfil = Perfil.objects.get(user=user)
            return self.filter(dono=perfil)
        except Perfil.DoesNotExist:
            return self.none()
