from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime

from .models import *
from .forms import *

from Clientes.models import *


import json

def lista_servicios(requets):
    lista_servicios = Servicios.objects.all()
    return render(requets, 'lista_servicios.html',{'lista_servicios':lista_servicios})



def detalle_servicio(request, servicio_id):
    '''Información detallada del servicio'''

    servicio = Servicios.objects.get(pk=servicio_id)
    
    context = {
        'servicio':servicio
    }
    return render(request, 'detalle_servicio.html', context)



def crear_servicio(request, cliente_id):
    '''Creamos un servicio en el sistema'''
    cliente = Cliente.objects.get(pk=cliente_id)
    dispositivos_cliente = Dispositivo.objects.filter(cliente=cliente.id)
    print(cliente)
    if request.method == 'POST':
        print('ingresamos al meth post de crear servicio e imprimimos')
        
        form = ServiciosForm(cliente, request.POST)
        
        
        if form.is_valid():
            print('ingresa a form valid')
            print(form)
            servicio = form.save()
            print(servicio.id)
            return redirect('detalle_servicio', servicio_id=servicio.id)

    else:
        print('ingresamos al form vacio de servicio')
       
        form = ServiciosForm(cliente)
    return render(request, 'servicio_form.html', {'form':form, 'cliente':cliente})
        
    


def editar_servicio(request, servicio_id):

    servicio = Servicios.objects.get(pk=servicio_id)
    if request.method == 'POST':
        form = ActualizarServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.save()
            return redirect('detalle_servicio', servicio_id=servicio.id)
    else:
        form = ActualizarServicioForm(instance=servicio)
        print(form)
    return render(request, 'editar_servicio.html', {'form':form})





def eliminar_servicio(request, servicio_id):
    '''Eliminamos un servicio'''

    servicio = Servicios.objects.get(pk=servicio_id)
    servicio.delete()
    return redirect('lista_servicios')




def lista_personas(request):
    if 'term' in request.GET:
        q = Cliente.objects.filter(identificacion__icontains = request.GET.get('term'))
        q_n = Cliente.objects.filter(nombres__icontains = request.GET.get('term'))
        identificaciones = list()
        nombres = list()
        if q:
            for cliente in q:
                identificaciones.append(cliente.identificacion + ' ' + cliente.nombres+' '+cliente.apellidos)
                
            return JsonResponse(identificaciones, safe=False)
        else:
            for cliente in q_n:
                nombres.append(cliente.identificacion + ' ' + cliente.nombres+' '+cliente.apellidos)
            return JsonResponse(nombres, safe=False)



def buscar_cliente(request):
    if request.method == 'POST':
        print('ingresamos al meth post de buscar cliente e imprimimos')
        print('---------------------')
        
        form = ClienteForm(request.POST)
        
        if form.is_valid():
            print('ingresamos a form valid')
            
            cliente = form.cleaned_data['cliente']
            espacios = cliente.find(' ')
            cliente = cliente[0:espacios]
            print(espacios)
            print(cliente)
            print(type(cliente))
            cliente = Cliente.objects.get(identificacion=cliente)
            print('el cliente es:')
            print(cliente.id)

            
              
            return redirect('crear_servicio', cliente_id=cliente.id)

    else:
        form = ClienteForm()
        print(form)
        
    return render(request, 'busqueda_cliente_form.html', {'form':form})

  


def iniciar_trabajo(request, servicio_id):
    servicio = Servicios.objects.get(pk=servicio_id)
    if request.method == 'POST':
        form = IniciarTrabajoForm(request.POST, instance=servicio)
        if form.is_valid():
            orden = form.save(commit=False)
            if orden.estado_orden.nombre == 'Finalizado':
                print('ingresa a if de finalizado')
                servicio.valor_total = servicio.valor_revision
                if servicio.abono < servicio.valor_total:
                    messages.warning(request, 'No se puede cerrar la orden de servicio con saldo pendiente por pagar...') 
                    return render(request, 'iniciar_trabajo.html',{'form':form})
                servicio.solucion_final = 'El cliente decidió no reparar el equipo, la orden queda cerrada'
                servicio.fecha_cierre_servicio = datetime.today()
            elif orden.estado_orden.nombre == 'Reparado':
                print('ingresa al if de reparado')
                if servicio.abono < servicio.valor_total:
                    messages.warning(request, 'No se puede cerrar la orden de servicio con saldo pendiente por pagar...') 
                    return render(request, 'iniciar_trabajo.html',{'form':form})
                servicio.fecha_cierre_servicio = datetime.today()
            servicio.saldo_pendiente = (orden.valor_total - (servicio.abono))
            orden.save()
            servicio.save()
            return redirect('detalle_servicio', servicio_id=servicio.id)
    else:
        form = IniciarTrabajoForm(instance=servicio)
    return render(request, 'iniciar_trabajo.html', {'form':form})





def dashboard(request):
    ordenes_servicio = Servicios.objects.all()
    total_orodenes_servicio = ordenes_servicio.count()
    ordenes_espera_revision = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Revisión')
    ordenes_en_revision = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Revisión')
    ordenes_espera_repuestos = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Repuestos')
    ordenes_espera_confirmacion_reparacion = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Confirmación de Reparación')
    ordenes_reparadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Reparado')
    ordenes_finalizadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Finalizado')
    
    #clientes
    clientes = Cliente.objects.all()
    total_clientes = clientes.count()
    clientes_ordenes_activas = Servicios.objects.exclude(estado_orden__nombre__icontains = 'Reparado').exclude(estado_orden__nombre__icontains = 'Finalizado')

    context = {
        
        'total_orodenes_servicio':total_orodenes_servicio,
        'ordenes_espera_revision':ordenes_espera_revision,
        'ordenes_en_revision':ordenes_en_revision,
        'ordenes_reparadas':ordenes_reparadas,
        'ordenes_finalizadas':ordenes_finalizadas,
        'ordenes_espera_repuestos':ordenes_espera_repuestos,
        'ordenes_espera_confirmacion_reparacion':ordenes_espera_confirmacion_reparacion,

        'total_clientes':total_clientes,
        'clientes_ordenes_activas':clientes_ordenes_activas,



    }

    return render(request,'dashboard.html', context)