from django.db import models

class Availability(models.Model):
    day = models.CharField('Dia', max_length=1,
                            choices= [
                                ("L", "Lunes"),
                                ("M", "Martes"),
                                ("X", "Miercoles"),
                                ("J", "Jueves"),
                                ("V", "Viernes"),
                                ("S", "Sabado"),
                                ("D", "Domingo"),
                                ])
    opening_time = models.TimeField("Hora de apertura")
    closing_time = models.TimeField("Hora de cierre")

