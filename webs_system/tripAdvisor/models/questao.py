from django.db import models
from .base_model import BaseModel
from .perfil import Perfil
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from ..enum import Status

class Questao(BaseModel):
    titulo = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    texto = models.TextField(validators=[MinLengthValidator(50)])
    status = models.CharField(max_length=20, choices=Status)
    data = models.DateField()
    lides = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    autor = models.ForeignKey(
        Perfil, 
        on_delete=models.CASCADE, 
        related_name='questoes_publicadas',
        verbose_name="Autor da Questão"
    )

    def __str__(self):
        return f"Titulo:{self.titulo} - Status:{self.status}"