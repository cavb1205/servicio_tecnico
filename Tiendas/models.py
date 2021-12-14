from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from datetime import *

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
    ciudad = models.CharField(max_length=100 ,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    administrador = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre



#suscripcion

class Membresia(models.Model):
    opciones_membresia = (
    ('Gratis','Gratis'),
    ('Mensual','Mensual'),
    ('Anual','Anual'),
    )
    nombre = models.CharField(max_length=100, choices=opciones_membresia)
    precio = models.DecimalField( max_digits=10 ,decimal_places=2, default=0)
    

    def __str__(self):
        todo = self.nombre + ' ' + str(self.precio) + ' ' + 'USD'
        return todo


class Tienda_membresia(models.Model):
    estado_choices = (
        ('Activa','Activa'),
        ('Vencida','Vencida'),
        ('Pendiente Pago','Pendiente Pago')
    )
    tienda = models.OneToOneField(Tienda, on_delete=models.CASCADE, 
                                    null=False, blank=False)
    membresia = models.ForeignKey(Membresia, on_delete=models.CASCADE)
    fecha_activacion = models.DateField()
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=50, choices=estado_choices, default=True)

    def __str__(self):
        return str(self.tienda) + ' - ' + str(self.membresia) 


    