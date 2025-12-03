from django.db import models
from .base_model import BaseModel
from .viagem import Viagem
from .categoria import Categoria
from .endereco import Endereco
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

class Atracao(BaseModel):
    nome = models.CharField(max_length=100, validators=[MinLengthValidator(5)])
    nota = models.FloatField()
    ingresso = models.BooleanField()
    valor = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    informacoes = models.TextField()
    site = models.URLField()
    telefone = models.CharField(max_length=11, blank=True, null=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL, 
        related_name='atracoes',
        null=True, 
        verbose_name="Categoria"
    )

    endereco = models.ForeignKey(
        'Endereco', 
        on_delete=models.SET_NULL,
        related_name='atracoes',
        blank=True,
        null=True, 
        verbose_name="Endereço Físico"
    )

    viagens = models.ManyToManyField(
        'Viagem', 
        related_name='atracoes_incluidas',
        verbose_name="Viagens Incluídas",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Atração"
        verbose_name_plural = "Atrações"

    def __str__(self):
        return f"Atração:{self.nome} - Nota:{self.nota}"
    
    def get_model_name(self):
        """Retorna o nome da classe do modelo (Ex: 'local' ou 'atividade') em minúsculas."""
        # Usa _meta.model_name que é a forma canônica e segura no Django
        return self._meta.model_name