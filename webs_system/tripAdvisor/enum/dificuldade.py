from django.db import models

class Dificuldade(models.TextChoices):
    EASY = "Fácil"
    MEDIUM = "Média"
    HARD = "Difícil"
    ULTRA_HARD = "Muito Difícil"
