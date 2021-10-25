from django.forms import ModelForm,fields, forms
from django import forms
from .models import *


class Tipo_ModeloForm(ModelForm):
    class Meta:
        model = Tipo_Modelo
        fields = '__all__'


class Modelo_DispositivoForm(ModelForm):
    class Meta:
        model = Modelo_Dispositivo
        fields = '__all__'
        widgets = {
            'marca': forms.Select(attrs={'class':'form-control'}),
            'modelo': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_modelo': forms.Select(attrs={'class':'form-control'}),
        }

class Color_DispositivoForm(ModelForm):
    class Meta:
        model = Color_Dispositivo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }


class DispositivoForm(ModelForm):
    class Meta:
        model = Dispositivo
        fields = [ 
            'modelo_dispositivo','serial','imei_principal','imei_opcional','direccion_mac','color_dispositivo','cliente'
        ]

    def __init__(self,cliente, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['serial']='N/A'
        self.initial['imei_principal']=0
        self.initial['imei_opcional']=0
        self.initial['direccion_mac']='N/A'
        self.initial['cliente'] = cliente

        self.fields['modelo_dispositivo'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )
        self.fields['serial'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['imei_principal'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['imei_opcional'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['direccion_mac'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['color_dispositivo'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['cliente'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )
        
class DispositivoIndividualForm(ModelForm):
    class Meta:
        model = Dispositivo
        fields = [ 
            'modelo_dispositivo','serial','imei_principal','imei_opcional','direccion_mac','color_dispositivo','cliente'
        ]

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['serial']='N/A'
        self.initial['imei_principal']=0
        self.initial['imei_opcional']=0
        self.initial['direccion_mac']='N/A'
        

        self.fields['modelo_dispositivo'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )
        self.fields['serial'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['imei_principal'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['imei_opcional'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['direccion_mac'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['color_dispositivo'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        
        )
        self.fields['cliente'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )
      