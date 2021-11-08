from django import forms
from django.db.models.query import QuerySet
from django.forms import ModelForm, fields, widgets

from Dispositivos.models import *
from .models import *
from .views import *
from Dispositivos.models import Dispositivo
from Servicios.models import Estado_Orden


class Problemas_FrecuentesForm(ModelForm):
    class Meta:
        model = Problemas_Frecuentes
        fields = '__all__'
        widgets = {
            'nombre_problema': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion_problema': forms.Textarea(attrs={'class':'form-control'}),
        }



class ClienteForm(forms.Form):
    cliente = forms.CharField()



class CrearDispositivoForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(CrearDispositivoForm, self).__init__(*args,**kwargs)
        self.initial['serial'] = 'N/A'
        self.initial['imei_principal'] = 'N/A'



    class Meta:
        model = Dispositivo
        fields = [
            'modelo_dispositivo', 'serial', 'imei_principal', 'color_dispositivo'
        ]

        widgets = {
            
            'modelo_dispositivo': forms.Select(attrs={'class':'form-control'}),
            'serial': forms.TextInput(attrs={'class':'form-control'}),
            'imei_principal': forms.TextInput(attrs={'class':'form-control'}),
            'color_dispositivo': forms.Select(attrs={'class':'form-control'}),
        }


class ActualizarServicioForm(ModelForm):
    class Meta:
        model = Servicios
        fields = ['dispositivo','fecha_entrega_estimada','estado_orden','problema_frecuente','observaciones','codigo_desbloqueo',
                'patron_desbloqueo','valor_revision','valor_total','abono','solucion_final',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class':'form-control'}),
            'dispositivo': forms.Select(attrs={'class':'form-control'}),
            'fecha_ingreso': forms.SelectDateWidget(attrs={'class':'form-control'}),
            'fecha_entrega_estimada': forms.DateInput(attrs={'class':'form-control'}),
            'estado_orden': forms.Select(attrs={'class':'form-control'}),
            'problema_frecuente': forms.Select(attrs={'class':'form-control'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control'}),
            'codigo_desbloqueo': forms.TextInput(attrs={'class':'form-control'}),
            'patron_desbloqueo': forms.TextInput(attrs={'class':'form-control'}),
            'valor_revision': forms.NumberInput(attrs={'class':'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class':'form-control'}),
            'abono': forms.NumberInput(attrs={'class':'form-control'}),
            'solucion_final': forms.Textarea(attrs={'class':'form-control'}),
        }


class ServiciosForm(ModelForm):
    def __init__(self, cliente,*args,**kwargs): 
        super (ServiciosForm,self ).__init__(*args,**kwargs) 
        self.initial['cliente'] = cliente
        self.fields['dispositivo'].queryset = Dispositivo.objects.filter(cliente=cliente.id)
        self.initial['valor_revision'] = 0
        self.initial['codigo_desbloqueo'] = 'N/A'
        #self.initial['estado_orden'] = Estado_Orden.objects.get(nombre__icontains='En Espera de Revisión')
    
    class Meta:
        model = Servicios
        fields = [
            'cliente','dispositivo','fecha_entrega_estimada','problema_frecuente','observaciones','codigo_desbloqueo','valor_revision','valor_total','abono'
        ]
        
        widgets = {
            
            'cliente': forms.Select(attrs={'class':'form-control'}),
            'dispositivo': forms.Select(attrs={'class':'form-control'}),
            'fecha_entrega_estimada': forms.DateInput(attrs={'class':'form-control'}),
            'estado_orden': forms.Select(attrs={'class':'form-control'}),
            'problema_frecuente': forms.Select(attrs={'class':'form-control'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control'}),
            'codigo_desbloqueo': forms.TextInput(attrs={'class':'form-control'}),
            'patron_desbloqueo': forms.TextInput(attrs={'class':'form-control'}),
            'valor_revision': forms.NumberInput(attrs={'class':'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class':'form-control'}),
            'abono': forms.NumberInput(attrs={'class':'form-control'}),
            'solucion_final': forms.Textarea(attrs={'class':'form-control'}),
        }


class IniciarTrabajoForm(ModelForm): 
    class Meta:
        model = Servicios 
        fields = ['fecha_entrega_estimada','estado_orden','abono','problema_frecuente','observaciones','valor_total','solucion_final','tecnico']
        widgets = {
            'fecha_entrega_estimada': forms.DateInput(attrs={'class':'form-control'}),
            'estado_orden': forms.Select(attrs={'class':'form-control'}),
            'abono': forms.NumberInput(attrs={'class':'form-control'}),
            'problema_frecuente': forms.Select(attrs={'class':'form-control'}),
            'observaciones': forms.Textarea(attrs={'class':'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class':'form-control'}),
            'solucion_final': forms.Textarea(attrs={'class':'form-control'}),
            'tecnico': forms.Select(attrs={'class':'form-control'}),
        }