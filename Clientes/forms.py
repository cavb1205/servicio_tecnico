from django.forms import ModelForm, fields
from .models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['identificacion','nombres','apellidos','email','telefono_principal','telefono_opcional','estado_cliente']
        