from django.db import models
from django.contrib.auth.models import User
from Tiendas.models import Tienda



class Perfil(models.Model):
    trabajador = models.OneToOneField(User, on_delete=models.CASCADE)
    identificacion = models.CharField(max_length=12)
    biografia = models.TextField(blank=True)
    telefono = models.CharField(max_length=15)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)

    def __str__(self):
        return self.identificacion

