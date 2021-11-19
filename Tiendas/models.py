from django.db import models
from django.contrib.auth.models import User


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Moneda(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=5)

    def __str__(self):
        return self.codigo + ' - ' + self.nombre


class Tienda(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, blank=True, null=True, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

