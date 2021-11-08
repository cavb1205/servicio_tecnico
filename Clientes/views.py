from .forms import ClienteForm, ClienteEditForm
from .models import Cliente

from Dispositivos.models import Dispositivo
from Servicios.models import Servicios

from django.db import models
from django.db.models.base import Model
from django.shortcuts import redirect, render
from django.contrib.auth.models import User




    
def lista_clientes(request):
    '''Lista todos los clientes activos'''

    lista_clientes = Cliente.objects.all()
    total_clientes = lista_clientes.count()
    context = {
        'lista_clientes':lista_clientes,
        'total_clientes':total_clientes,
    }
    return render(request, 'lista_clientes.html', context)


def detalle_cliente(request, cliente_id):
    '''Información detallada del cliente'''

    cliente = Cliente.objects.get(pk=cliente_id)
    dispositivos = Dispositivo.objects.filter(cliente=cliente.id)
    servicios = Servicios.objects.filter(cliente=cliente.id).order_by('-fecha_ingreso')
    total_ordenes = servicios.count()

    context = {
        'cliente':cliente,
        'dispositivos':dispositivos,
        'servicios':servicios,
        'total_ordenes':total_ordenes,
    }
    return render(request, 'detalle_cliente.html', context)



def crear_cliente(request):
    '''Creamos un cliente en el sistema'''
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        
        if form.is_valid():
            cliente = form.save()
            print(cliente.id)
            return redirect('detalle_cliente', cliente_id=cliente.id)

    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form':form})


def crear_cliente_servicio(request):
    '''Creamos un cliente en el sistema'''
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        
        if form.is_valid():
            cliente = form.save()
            print(cliente.id)
            return redirect('crear_servicio', cliente_id=cliente.id)

    else:
        form = ClienteForm()
    return render(request, 'cliente_form.html', {'form':form})


def editar_cliente(request, cliente_id):

    cliente = Cliente.objects.get(pk=cliente_id)
    if request.method == 'POST':
        form = ClienteEditForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = ClienteEditForm(instance=cliente)
        print(form)
    return render(request, 'editar_cliente_form.html', {'form':form})





def eliminar_cliente(request, cliente_id):
    '''Eliminamos un cliente'''

    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')







