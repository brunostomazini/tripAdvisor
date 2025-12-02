from django.db import models

class Turno(models.TextChoices):
    MANHA = "Manhã"
    TARDE = "Tarde"
    NOITE = "Noite"