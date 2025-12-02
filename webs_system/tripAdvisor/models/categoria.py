from django.db import models
from .base_model import BaseModel
from django.core.validators import MinLengthValidator, MinValueValidator
from ..enum import Classificacao


class Categoria(BaseModel):
    nome = models.CharField(max_length=50, validators=[MinLengthValidator(5)])
    classificacao = models.CharField(max_length=20, choices=Classificacao)
    descricao = models.TextField()

    def __str__(self):
        return f"Categoria:{self.nome} Classificação:{self.classificacao}"
