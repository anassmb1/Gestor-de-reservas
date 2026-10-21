from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from pistas.models import Pista
from availability.models import Availability

class Booking(models.Model):
    user = models.ForeignKey(User,verbose_name='Usuario' ,on_delete=models.CASCADE, related_name='bookings')
    court = models.ForeignKey(Pista,verbose_name='Número de pista' ,on_delete=models.CASCADE, related_name='bookings')
    start_datetime = models.DateTimeField('Hora de la reserva')
    end_datetime = models.DateTimeField('Hora a la que termina la reserva')
    type = models.CharField("Estado de la reserva", choices=[ ("ACTIVE", "Activa"),("FINISHED", "Finalizada"),("CANCELED","Cancelada")])

    class Meta:
        ordering = ['start_datetime']
    
    def clean(self):
        super().clean()

        #Aqui validamos que los tiempos de reserva sean en horas exactas 
        if self.start_datetime.minute != 0 or self.start_datetime.second != 0:
            raise ValidationError("La reserva debe comenzar y terminar a una hora exacta.")

        #Aqui validamos que la hora a la que empieza y acaba la reserva son del mismo dia
        if self.start_datetime.date() != self.end_datetime.date():
            raise ValidationError("Error")

        #Aqui validamos que la hora a la que empieza es antes de la hora a la que acaba
        if self.start_datetime >= self.end_datetime:
            raise ValidationError("Error")
        
        #Aqui validamos que las horas de la reserva esten dentro del horario de apertura
        dias = ["L","M","X","J","V","S","D"]
        dia = dias[self.start_datetime.weekday()]

        try:
            availability = Availability.objects.get(day=dia)
        except Availability.DoesNotExist:
            raise ValidationError("No existe el horario.")
        
        hora_inicio = self.start_datetime.time()
        hora_fin = self.end_datetime.time()

        if hora_inicio < availability.opening_time:
            raise ValidationError("Error")
        
        if hora_fin > availability.closing_time:
            raise ValidationError("Error")
        
        