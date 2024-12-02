from django import forms
from .models import Libro
from datetime import date  # Importa la clase date

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'opinion', 'tag', 'puntuacion', 'foto_url', 'fecha_termino', 'fecha_agregada']
    
    # Campo de fecha de término con selector de fecha
    fecha_termino = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False  # Si quieres que sea opcional
    )
    
    # Campo de fecha agregada con la fecha de hoy por defecto
    fecha_agregada = forms.DateField(
        widget=forms.HiddenInput(),  # Oculto en el formulario, pero se envía
        initial=date.today  # Establece la fecha actual
    )

    # Cambiar el campo 'descripcion' a 'opinion'
    opinion = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe tu opinión sobre el libro'}))

    # Campo opcional para la URL de la foto
    foto_url = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': 'URL de la foto'}))

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