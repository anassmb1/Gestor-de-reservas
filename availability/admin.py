from django.contrib import admin
from .models import Availability

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['day']
