from django.db import models
from django.db.models.fields import DecimalField
from Clientes.models import *
from Dispositivos.models import *
from datetime import date

# Create your models here.


class Problemas_Frecuentes(models.Model):
    nombre_problema = models.CharField(max_length=200)
    descripcion_problema = models.TextField(blank=True)

    def __str__(self):
        return self.nombre_problema


class Estado_Orden(models.Model):
    '''Nombre estados de la orden (Activo, revision, finalizado, cancelado)'''

    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Servicios(models.Model):
    '''Ordenes de servicio tecnico'''

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, null=True)
    fecha_ingreso = models.DateTimeField(default=date.today())
    fecha_entrega_estimada = models.DateField(auto_now=False, auto_now_add=False, blank=True, default=date.today())
    estado_orden = models.ForeignKey(Estado_Orden, on_delete=models.CASCADE)
    problema_frecuente = models.ForeignKey(Problemas_Frecuentes, on_delete=models.CASCADE, blank=True, null=True)
    observaciones = models.TextField(max_length=250, blank=True)
    codigo_desbloqueo = models.CharField(max_length=10, blank=True)
    patron_desbloqueo = models.IntegerField(blank=True)
    valor_revision = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    abono = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    fecha_cierre_servicio = models.DateTimeField(null=True, blank=True)
    solucion_final = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.observaciones