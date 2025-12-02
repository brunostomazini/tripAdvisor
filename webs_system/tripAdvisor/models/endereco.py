from django.db import models
from .base_model import BaseModel
from django.core.validators import MinLengthValidator, MinValueValidator


class Endereco(BaseModel):
    cep = models.CharField(max_length=8, validators=[MinLengthValidator(8)])
    logradouro = models.CharField(max_length=50, validators=[MinLengthValidator(5)])
    numero = models.IntegerField(validators=[MinValueValidator(0)])
    complemento = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    bairro = models.CharField(max_length=30, validators=[MinLengthValidator(5)])
    cidade = models.CharField(max_length=30, validators=[MinLengthValidator(3)])
    estado = models.CharField(max_length=30, validators=[MinLengthValidator(5)])
    pais = models.CharField(max_length=100, validators=[MinLengthValidator(3)])

    def __str__(self):
        return f"{self.cidade} {self.estado} numero:{self.numero} "