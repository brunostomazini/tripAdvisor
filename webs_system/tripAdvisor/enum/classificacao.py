from django.db import models

class Classificacao(models.TextChoices):
    GENERAL = "Geral"
    FAMILIES = "Famílias"
    COUPLES = "Casais"
    SOLO = "Solo"
    BUSINESS = "Negócios"
    ADULT ="Adulto"