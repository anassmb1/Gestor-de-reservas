from django import forms
from django.contrib.auth.models import User

from profiles.models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    birth_date = forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type':'date'}))
    phone_number = forms.CharField(label="Número de teléfono", max_length=20)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

    def save(self, commit=True):
        user = super().save(commit=False) 
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                birth_date=self.cleaned_data["birth_date"],
                phone_number=self.cleaned_data["phone_number"]
                )
            
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())