from django.db.models import fields
import django_filters

from django import forms
from django_filters.filters import ChoiceFilter, ModelChoiceFilter

from Servicios.models import Servicios
from Clientes.models import Cliente
from Dispositivos.models import Dispositivo
from Tiendas.models import Membresia, Tienda_membresia


class ServicioFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"# Orden"}))
    
    class Meta:
        model = Servicios
        fields = ['id']



class ClienteFilter(django_filters.FilterSet):
    identificacion = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"# Identificación Cliente"}))
    
    class Meta:
        model = Cliente
        fields = ['identificacion']



class DispositivoFilter(django_filters.FilterSet):
    serial = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"# Serie Dispositivo"}))
    
    class Meta:
        model = Dispositivo
        fields = ['serial']



class TiendaFilter(django_filters.FilterSet):
    ESTADO_CHOICES = (
        ('Activa','Activa'),
        ('Vencida','Vencida'),
        ('Pendiente Pago','Pendiente Pago')
    )
    tienda__nombre = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Nombre Tienda"}))
    membresia = ModelChoiceFilter(queryset=Membresia.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    estado = ChoiceFilter(choices=ESTADO_CHOICES,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Tienda_membresia
        fields = ['tienda__nombre','membresia','estado']