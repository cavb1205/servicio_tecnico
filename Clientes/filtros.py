from django.forms import widgets
import django_filters
from django import forms
from .models import Cliente


class ClienteFilter(django_filters.FilterSet):
    identificacion = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"No. Identificación"}))
    nombres = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Nombres"}))
    apellidos = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Apellidos"}))

    class Meta:
        model = Cliente
        fields = ['identificacion','nombres','apellidos']
       