from django.db import models

from Clientes.models import *




class Tipo_Modelo(models.Model):
    '''Tipo modelo dispositivo'''

    nombre_tipo_modelo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_tipo_modelo

class Marca_Dispositivo(models.Model):
    nombre_marca =  models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_marca


class Modelo_Dispositivo(models.Model):
    '''Nombre modelo del dispositivo'''

    marca = models.ForeignKey(Marca_Dispositivo, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=100)
    tipo_modelo = models.ForeignKey(Tipo_Modelo, on_delete=models.CASCADE)

    def __str__(self):
        modelos = str(self.marca.nombre_marca) + ' '+ self.modelo 
        
        return modelos


class Color_Dispositivo(models.Model):

    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Dispositivo(models.Model):
    '''informacion basica del dispositivo'''

    modelo_dispositivo = models.ForeignKey(Modelo_Dispositivo, on_delete=models.CASCADE)
    serial = models.CharField(max_length=100)
    imei_principal = models.BigIntegerField()
    imei_opcional = models.BigIntegerField(blank=True, null=True)
    direccion_mac = models.CharField(max_length=20, blank=True)
    color_dispositivo = models.ForeignKey(Color_Dispositivo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.modelo_dispositivo) + ' ' + str(self.color_dispositivo) 