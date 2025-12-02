from django.db import models

class Status(models.TextChoices):
    NOT_ANSWERED = "Não Respondida"
    ANSWERED = "Respondida"
    ARCHIVED = "Arquivada"
    CLOSED = "Fechada"
    MODERATED = "Moderada"
    FLAGGED = "Sinalizada"