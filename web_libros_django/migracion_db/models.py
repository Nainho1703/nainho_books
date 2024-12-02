from django.db import models
from django.contrib.auth.models import User

class Libro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='libros', null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    autor = models.CharField(max_length=255, null=True, blank=True)
    tipo = models.CharField(max_length=255, null=True, blank=True)
    fecha_termino = models.DateField(null=True, blank=True)
    puntuacion = models.FloatField(null=True, blank=True)
    opinion = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=1000, null=True, blank=True)
    fecha_agregada = models.DateField(null=True, blank=True)
    foto_url = models.URLField()

    def __str__(self):
        return f"{self.titulo} ({self.user.username})"

from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_data')
    data_field = models.CharField(max_length=255)  # Personaliza este campo según tu necesidad
    created_at = models.DateTimeField(auto_now_add=True)  # Marca temporal automática

    def __str__(self):
        return f"{self.user.username} - {self.data_field}"
