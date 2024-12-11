from django import forms
from .models import Libro
from datetime import date

class LibroForm(forms.ModelForm):
    # Bloquear los campos de título, autor y foto_url
    titulo = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    autor = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    foto_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'readonly': 'readonly'}))

    # Nuevo campo para la URL que el usuario introducirá
    url_libro = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': 'Introduce la URL del libro'}))

    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'opinion', 'tag', 'puntuacion', 'foto_url', 'fecha_termino', 'fecha_agregada', 'url_libro']
    
    # Campo de fecha de término con selector de fecha
    fecha_termino = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False
    )
    
    # Campo de fecha agregada con la fecha de hoy por defecto
    fecha_agregada = forms.DateField(
        widget=forms.HiddenInput(),  
        initial=date.today
    )

    # Campo de opinión
    opinion = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu opinión sobre el libro'}))

from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data