from django.forms import ModelForm, fields
from django import forms
from .models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'identificacion': forms.TextInput(attrs={'class':'form-control'}),
            'nombres': forms.TextInput(attrs={'class':'form-control'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'telefono_principal': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_opcional': forms.TextInput(attrs={'class':'form-control'}),
            'estado_cliente' : forms.Select(attrs={'class':'form-control'}),

        }
        
    def __init__(self,*args,**kwargs):
        super(ClienteForm, self).__init__(*args,**kwargs)
        self.initial['telefono_principal'] = '+56'
        self.initial['telefono_opcional'] = '+56'
        self.initial['email'] = 'ejemplo@gmail.com'



class ClienteEditForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'identificacion': forms.TextInput(attrs={'class':'form-control'}),
            'nombres': forms.TextInput(attrs={'class':'form-control'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'telefono_principal': forms.TextInput(attrs={'class':'form-control'}),
            'telefono_opcional': forms.TextInput(attrs={'class':'form-control'}),
            'estado_cliente' : forms.Select(attrs={'class':'form-control'}),

        }