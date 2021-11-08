from django.db.models.base import Model
from django.forms import ModelForm, widgets

from Trabajadores.models import Perfil
from django.contrib.auth.models import User
from django import forms




class TrabajadorForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','groups','is_active','is_superuser',]
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'groups':forms.SelectMultiple(attrs={'class':'form-control'}),
        }







class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['identificacion','biografia','telefono']
        widgets = {
            'identificacion':forms.TextInput(attrs={'class':'form-control'}),
            'biografia':forms.Textarea(attrs={'class':'form-control'}),
            'telefono':forms.TextInput(attrs={'class':'form-control'}),
        }
