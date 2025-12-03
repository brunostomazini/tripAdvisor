from django.db import models
from .base_model import BaseModel
from .atracao import Atracao
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from ..enum import Dificuldade
from ..enum import Turno
from ..managers.atividade_manager import AtividadeManager

class Atividade(Atracao):
    turno = models.CharField(max_length=20, choices=Turno)
    duracao = models.TimeField()
    guia = models.BooleanField()
    participantes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    dificuldade = models.CharField(max_length=20, choices=Dificuldade)

    objects = AtividadeManager()

    class Meta:
        verbose_name = "Atividade"
        verbose_name_plural = "Atividades"
        
        
    
    def __str__(self):
        return f"Atividade:{self.nome}"