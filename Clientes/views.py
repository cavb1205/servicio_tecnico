from .forms import ClienteForm
from .models import Cliente
from django.db import models
from django.db.models.base import Model
from django.shortcuts import redirect, render



    
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


def editar_cliente(request, cliente_id):

    cliente = Cliente.objects.get(pk=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.save()
            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente_form.html', {'form':form})





def eliminar_cliente(request, cliente_id):
    '''Eliminamos un cliente'''

    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()
    return redirect('lista_clientes')


