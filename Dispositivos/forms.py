from django.forms import ModelForm,fields, forms
from django import forms
from .models import *
from Clientes.models import Cliente



class Tipo_ModeloForm(ModelForm):
    class Meta:
        model = Tipo_Modelo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }


class Color_DispositivoForm(ModelForm):
    class Meta:
        model = Color_Dispositivo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }



class MarcaForm(ModelForm):
    class Meta:
        model = Marca_Dispositivo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'})
        }


class DispositivoForm(ModelForm):
    class Meta:
        model = Dispositivo
        fields = [ 
            'marca','modelo_dispositivo','tipo','serial','imei_principal','imei_opcional','direccion_mac','color_dispositivo',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['serial']='N/A'
        self.initial['imei_principal']=0
        self.initial['imei_opcional']=0
        self.initial['direccion_mac']='N/A'
        

        self.fields['marca'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )
        self.fields['modelo_dispositivo'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )
        self.fields['tipo'].widget.attrs.update(
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
        
        
class DispositivoIndividualForm(ModelForm):
    class Meta:
        model = Dispositivo
        fields = [ 
            'marca','modelo_dispositivo','tipo','serial','imei_principal','imei_opcional','direccion_mac','color_dispositivo','cliente'
        ]

    def __init__(self,tienda,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['serial']='N/A'
        self.initial['imei_principal']=0
        self.initial['imei_opcional']=0
        self.initial['direccion_mac']='N/A'
        self.fields['cliente'].queryset = Cliente.objects.filter(tienda=tienda.id)
        

        self.fields['marca'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )

        self.fields['modelo_dispositivo'].widget.attrs.update(
            {
                'class': 'form-control',
                
            }
        )
        self.fields['tipo'].widget.attrs.update(
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
      

class EditarDispositivoForm(ModelForm):
    class Meta:
        model = Dispositivo
        fields = [ 
            'marca','modelo_dispositivo','tipo','serial','imei_principal','imei_opcional','direccion_mac','color_dispositivo',
        ]
        widgets = {
            'marca': forms.Select(attrs={'class':'form-control'}),
            'modelo_dispositivo': forms.TextInput(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'serial': forms.TextInput(attrs={'class':'form-control'}),
            'imei_principal': forms.TextInput(attrs={'class':'form-control'}),
            'imei_opcional': forms.TextInput(attrs={'class':'form-control'}),
            'direccion_mac': forms.TextInput(attrs={'class':'form-control'}),
            'color_dispositivo': forms.Select(attrs={'class':'form-control'}),
            


        }

      