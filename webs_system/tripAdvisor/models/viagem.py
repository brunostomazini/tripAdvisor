from django.db import models
from .base_model import BaseModel
from django.core.validators import MinLengthValidator, MinValueValidator
from django.core.exceptions import ValidationError
from ..enum import *
from datetime import date
from .perfil import Perfil
from .atracao import Atracao
from ..managers.viagem_manager import ViagemManager


class Viagem(BaseModel):
    titulo = models.CharField(max_length=50, validators=[MinLengthValidator(5)])
    descricao = models.TextField(blank=True, null=True)
    destino = models.CharField(max_length=100, validators=[MinLengthValidator(3)],blank=True, null=True)
    pais_destino = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    inicio = models.DateField(validators=[MinValueValidator(date.today(), message="A data de início não pode ser no passado.")])
    final = models.DateField()
    orcamento = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0, message='O orçamento deve ser zero ou um valor positivo.')])
    proposito = models.CharField(max_length=20, choices=Proposito)
    notas = models.TextField(blank=True, null=True)
    transporte = models.CharField(max_length=20, choices=Transporte)
    ##Viajante
    dono = models.ForeignKey(
        Perfil, 
        on_delete=models.CASCADE, 
        related_name='viagens',
        verbose_name="Dono da Viagem" 
    )

    atracoes = models.ManyToManyField(
        Atracao, 
        related_name='viagens', 
        verbose_name="Atrações da Viagem",
        blank=True,
        null=True
    )

    objects = ViagemManager()

    def __str__(self):
        return f"Titulo:{self.titulo} - Destino:{self.destino} - Descrição:{self.descricao}"
    
    def clean(self):
        super().clean()
        
        if self.inicio and self.final:
            if self.final < self.inicio:
                raise ValidationError({
                    'final': "A data final deve ser posterior à data de início."
                })