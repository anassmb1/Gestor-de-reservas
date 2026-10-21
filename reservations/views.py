from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic import ListView, DetailView
from django.contrib import messages

from .models import Booking
from .forms import BookingForm

class CreateBookingView(CreateView):
    template_name = "booking/booking_create.html"
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ListBookingView(ListView):
    template_name = "booking/booking_list.html"
    model = Booking
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    
class UpdateBookingView(UpdateView):
    model = Booking
    template_name = "booking/booking_update.html"
    form_class = BookingForm
    success_url = reverse_lazy('booking_list')

    def dispatch(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.user != self.request.user:
            return HttpResponseRedirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Reserva actualizada")
        return super(UpdateBookingView, self).form_valid(form)
    