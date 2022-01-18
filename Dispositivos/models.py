from django.db import models

from Clientes.models import *
from Tiendas.models import Tienda




class Tipo_Modelo(models.Model):
    '''Tipo modelo dispositivo'''

    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Marca_Dispositivo(models.Model):
    nombre =  models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Color_Dispositivo(models.Model):

    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    '''informacion basica del dispositivo'''

    marca = models.ForeignKey(Marca_Dispositivo, on_delete=models.CASCADE)
    modelo_dispositivo = models.CharField(max_length=100,)
    tipo = models.ForeignKey(Tipo_Modelo, on_delete=models.CASCADE)
    serial = models.CharField(max_length=100)
    imei_principal = models.BigIntegerField()
    imei_opcional = models.BigIntegerField(blank=True, null=True)
    direccion_mac = models.CharField(max_length=20, blank=True)
    color_dispositivo = models.ForeignKey(Color_Dispositivo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.marca) + ' ' + str(self.modelo_dispositivo) + ' ' + str(self.color_dispositivo) 