from django.db import models
from django.forms import fields
from django.forms.widgets import Widget
import django_filters
from django import forms

from django.contrib.auth.models import User
from .models import Perfil


class PerfilFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Nombres"}))
    last_name = django_filters.CharFilter(lookup_expr='icontains',widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Apellidos"}))
    
    
    class Meta:
        model = User
        fields = ['first_name','last_name']