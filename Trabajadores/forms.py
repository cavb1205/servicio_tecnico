from django.contrib.auth import models
from django.db.models.base import Model
from django.forms import ModelForm, fields, widgets

from Trabajadores.models import Perfil
from django.contrib.auth.models import User
from django import forms


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password',]
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
        
class PasswordForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = 'Nueva Contraseña'

    class Meta:
        model = User
        fields = ['password',]
        widgets = {'password':forms.PasswordInput(attrs={'class':'form-control'}),}


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
