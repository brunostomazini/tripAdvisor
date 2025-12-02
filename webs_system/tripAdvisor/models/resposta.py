from django.db import models
from .base_model import BaseModel
from .perfil import Perfil
from .questao import Questao
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator


class Resposta(BaseModel):
    titulo = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    texto = models.TextField(validators=[MinLengthValidator(50)])
    data = models.DateField()
    lides = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    questao = models.ForeignKey(
        Questao, 
        on_delete=models.CASCADE, 
        related_name='respostas',
        verbose_name="Questão Respondida"
    )
    
    
    autor = models.ForeignKey(
        Perfil, 
        on_delete=models.CASCADE, 
        related_name='respostas_escritas',
        verbose_name="Autor da Resposta"
    )

    def __str__(self):
        return f"Titulo:{self.titulo}"