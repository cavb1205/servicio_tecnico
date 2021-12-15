from django.db.models import fields
import django_filters

from django import forms

from Servicios.models import Servicios
from Clientes.models import Cliente
from Dispositivos.models import Dispositivo


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