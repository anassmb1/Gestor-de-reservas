from django.db import models

class Pista(models.Model):
    name = models.CharField("Número pista", max_length=50)
    type = models.CharField("Tipo de pista", choices=[ ("INDOOR", "Indoor"),("OUTDOOR", "Outdoor")])

    def __str__(self):
        return f'{self.name}'