from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.views.generic.edit import CreateView

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import *

class HomeView(TemplateView):
    template_name = "home.html"

class RegisterView(CreateView):
    template_name = "register.html"
    model = User
    success_url = reverse_lazy('home')
    form_class = RegisterForm 

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil creado")
        return super(RegisterView, self).form_valid(form)

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self,form):
        usuario = form.cleaned_data.get('username')
        contraseña = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=contraseña)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f"Bienvenido {usuario}")
            return redirect('home')
        
        messages.add_message(self.request, messages.ERROR, "Usuario y/o contraseña no válidos")
        return self.form_invalid(form)
    
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, f"Sesión cerrada correctamente")
    return redirect('login')