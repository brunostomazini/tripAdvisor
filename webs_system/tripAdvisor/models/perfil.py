from django.db import models
from .base_model import BaseModel
from ..enum import *
from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

class Perfil(BaseModel):
    email = models.CharField(max_length=100, validators=[MinLengthValidator(10)])
    nome = models.CharField(max_length=100, validators=[MinLengthValidator(10)])
    passaporte = models.CharField(max_length=10, validators=[MinLengthValidator(10)])
    data_nascimento = models.DateField()
    pais = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    genero = models.CharField(max_length=20, choices=Genero, default=Genero.NOT_INFORMED)
    pagina_pessoal = models.URLField(max_length=150, validators=[MinLengthValidator(15)], blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    lingua = models.CharField(max_length=20, validators=[MinLengthValidator(5)], blank=True, null=True)
    premium = models.BooleanField(default=False)
    membro_desde = models.DateField(auto_now_add=True)

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True,

    )

    def __str__(self):
        return f"Nome:{self.nome} - E-mail:{self.email}" 

    def clean(self):
        if self.data_nascimento:
            adulto = date.today().replace(year=date.today().year - 18)

            if self.data_nascimento > adulto:
                raise ValidationError({'data_nascimento':"Usuario precisa ter 18 anos ou mais!"})