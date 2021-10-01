from .models import Cliente
from django.db import models
from django.db.models.base import Model
from django.shortcuts import render



    
def lista_clientes(request):
    '''Lista todos los clientes activos'''

    lista_clientes = Cliente.objects.all()
    context = {
        'lista_clientes':lista_clientes
    }
    return render(request, 'lista_clientes.html', context)


def detalle_cliente(request, cliente_id):
    '''Información detallada del cliente'''

    cliente = Cliente.objects.get(pk=cliente_id)
    print(cliente.nombres)

    context = {
        'cliente':cliente
    }
    return render(request, 'detalle_cliente.html', context)