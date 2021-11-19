from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
from django import forms
from Tiendas.models import Tienda



class AdminTiendaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminTiendaForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }


class TiendaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TiendaForm, self).__init__(*args,**kwargs)
        self.fields['nombre'].label = 'Nombre de la tienda'
        
        self.initial['telefono'] = '+56'


    class Meta:
        model = Tienda
        fields = [ 
            'nombre',
            'direccion',
            'ciudad',
            
            'telefono',
            'moneda',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'ciudad': forms.Select(attrs={'class':'form-control'}),
            
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(attrs={'class':'form-control'}),
        }

