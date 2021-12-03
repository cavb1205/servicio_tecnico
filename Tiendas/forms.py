from django.contrib.auth.models import User
from django.forms import ModelForm, widgets
from django import forms
from Tiendas.models import Membresia, Tienda, Tienda_membresia



class AdminTiendaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminTiendaForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['password'].label = 'Contraseña'
        

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','password']
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'})
        }


class TiendaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TiendaForm, self).__init__(*args,**kwargs)
        self.fields['nombre'].label = 'Nombre de la tienda'
        
        


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
            'ciudad': forms.TextInput(attrs={'class':'form-control'}),
            
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'moneda': forms.Select(attrs={'class':'form-control'}),
        }


class MembresiaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MembresiaForm, self).__init__(*args, **kwargs)
        self.fields['membresia'].queryset = Membresia.objects.exclude(nombre='Gratis')
    class Meta:
        model = Tienda_membresia
        fields = ['membresia']
        widgets = {
            'membresia': forms.Select(attrs={'class':'form-control'}),
        }