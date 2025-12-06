from django.db import models
from .base_model import BaseModel
from .atracao import Atracao
from django.core.validators import MinLengthValidator, MinValueValidator
from ..enum import Classificacao
from ..managers.local_manager import LocalManager


class Local(Atracao):
    horario_abertura = models.TimeField()
    horario_fechamento = models.TimeField()
    acessibilidade = models.BooleanField()
    classificacao = models.CharField(max_length=20, choices=Classificacao)

    objects = LocalManager()

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locais"
        
    def __str__(self):
        return f"Local:{self.nome}"
    
    def get_model_name(self):
        return 'local'