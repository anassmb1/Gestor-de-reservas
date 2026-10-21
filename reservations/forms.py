from django import forms
from django.core.exceptions import ValidationError
import random

from .models import Booking
from pistas.models import Pista

class BookingForm(forms.ModelForm):
    court_type = forms.ChoiceField(
        label="Tipo de pista",
        choices=[
            ("INDOOR", "Indoor"),
            ("OUTDOOR", "Outdoor"),
        ]
    )

    class Meta:
        model = Booking
        fields = ["start_datetime", "end_datetime"]

        widgets = {
            "start_datetime": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "step": "1800"}
            ),
            "end_datetime": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "step": "1800"}
            ),
        }

    #Aqui validamos que hay al menos una pista disponible para el tipo y hora solicitados
    def save(self, commit=True):
        booking = super().save(commit=False)
        court_type = self.cleaned_data["court_type"]

        court_type = court_type
        start_datetime = booking.start_datetime
        end_datetime = booking.end_datetime

        reservas_solapadas = Booking.objects.filter(
            court__type=court_type,
            start_datetime__lt=end_datetime,
            end_datetime__gt=start_datetime,
            type="ACTIVE",
        )

        if booking.pk:
            reservas_solapadas = reservas_solapadas.exclude(
                pk=booking.pk
            )
    
        pistas_ocupadas = reservas_solapadas.values_list(
            "court_id", 
            flat=True
        )

        pistas_disponibles = Pista.objects.filter(type=court_type).exclude(
            id__in=pistas_ocupadas
        )

        if not pistas_disponibles.exists():
            raise ValidationError("No hay pistas disponibles de este tipo en ese horario.")
        
        pista_libre = random.choice(list(pistas_disponibles))
        booking.court = pista_libre
        booking.type = "ACTIVE"

        if commit:
            booking.save()
        return booking
    
