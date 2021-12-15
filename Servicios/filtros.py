from django.db.models.fields import DateField
import django_filters
from django_filters import ModelChoiceFilter
from django import forms

from Dispositivos.models import Dispositivo


from .models import Estado_Orden, Servicios, Problemas_Frecuentes
from Clientes.models import Cliente


class ServiciosFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"# Orden"}))
    cliente__nombres = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Cliente"}))
    dispositivo = ModelChoiceFilter(queryset=Dispositivo.objects.all(),widget=forms.Select(attrs={'class':'form-control','placeholder':"Cliente"}))
    problema_frecuente = ModelChoiceFilter(queryset=Problemas_Frecuentes.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    estado_orden = ModelChoiceFilter(queryset=Estado_Orden.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Servicios
        fields = ['id','cliente__nombres','dispositivo','problema_frecuente','estado_orden']