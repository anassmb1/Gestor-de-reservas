from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='Usuario')
    birth_date = models.DateField('Fecha de nacimiento')
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user}'