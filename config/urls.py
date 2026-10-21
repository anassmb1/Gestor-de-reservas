from django.contrib import admin
from django.urls import path

from core.views import *
from reservations.views import CreateBookingView, ListBookingView, UpdateBookingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),
    path('booking/create/', CreateBookingView.as_view(), name="booking_create"),
    path('booking/list/', ListBookingView.as_view(), name="booking_list"),    
    path('booking/update/<int:pk>', UpdateBookingView.as_view(), name="booking_update"),  
]
