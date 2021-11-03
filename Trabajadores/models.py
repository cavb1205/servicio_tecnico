from django.db import models
from django.contrib.auth.models import User



class Perfil(models.Model):
    trabajador = models.OneToOneField(User, on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=12)
    biografia = models.TextField(blank=True)
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.identificacion

