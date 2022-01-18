import django_filters
from django_filters import ModelChoiceFilter
from django import forms


from .models import *


class DispositivoFilter(django_filters.FilterSet):
    marca = ModelChoiceFilter(widget=forms.Select(attrs={'class':'form-control','placeholder':"Marca"}),queryset=Marca_Dispositivo.objects.all())
    modelo_dispositivo = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Modelo"}))
    color_dispositivo = ModelChoiceFilter(queryset=Color_Dispositivo.objects.all(),widget=forms.Select(attrs={'class':'form-control','placeholder':"Color"}))
    serial = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Serial"}))
    imei_principal = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Imei"}))
    
    
    class Meta:
        model = Dispositivo
        fields = ['marca','modelo_dispositivo','color_dispositivo','serial','imei_principal']