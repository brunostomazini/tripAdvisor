from django.db import models
from .base_model import BaseModel
from .perfil import Perfil
from .atracao import Atracao
from datetime import date
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from ..managers.avaliacao_manager import AvaliacaoManager

class Avaliacao(BaseModel):
    titulo = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    texto = models.TextField(validators=[MinLengthValidator(50)])
    nota = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    data_visita = models.DateField()
    data_avaliacao = models.DateField(default=date.today())
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    atracao = models.ForeignKey(
        Atracao,
        on_delete=models.CASCADE,
        related_name='avaliacoes_recebidas',
        verbose_name="Atração Avaliada"
    )

    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name='avaliacoes_feitas',
        verbose_name="Perfil Avaliador"
    )

    objects = AvaliacaoManager()

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        unique_together = ('perfil', 'atracao')
    
    def __str__(self):
        return f"Titulo:{self.titulo} - Nome:{self.perfil.nome}"