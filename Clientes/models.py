from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from Tiendas.models import Tienda



class Estado_Cliente(models.Model):
    '''Estados del cliente en el sistema'''

    nombre_estado = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_estado


class Cliente(models.Model):
    '''informacion personal de un cliente(datos personales de contacto)'''

    identificacion = models.CharField(max_length=12, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    telefono_principal = models.CharField(max_length=15)
    telefono_opcional = models.CharField(max_length=15, blank=True)
    estado_cliente = models.ForeignKey(Estado_Cliente, on_delete=models.CASCADE, default=1)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)

    def __str__(self):
        nombres = (self.nombres)
        apellidos = self.apellidos 
        identificacion = self.identificacion
        cliente = (nombres+' ' + apellidos + ' ' + identificacion)
        return cliente


