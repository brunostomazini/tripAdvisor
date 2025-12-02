from django.db import models

class Transporte(models.TextChoices):
    TRAIN = "Trem"
    PLANE = "Avião"
    CAR = "Carro"
    BUS = "Ônibus"
    SEVERAL = "Diversos"