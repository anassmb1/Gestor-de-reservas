from django.contrib import admin
from .models import Pista

@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ['name', 'type' ]
