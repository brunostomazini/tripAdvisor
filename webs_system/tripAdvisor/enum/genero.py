from django.db import models


class Genero(models.TextChoices):
    MAN = "Homen"
    WOMAN = "Mulher"
    NON_BINARY = "Não Binario"
    NOT_INFORMED = "Não informado"
