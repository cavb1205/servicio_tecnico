from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *

from Clientes.models import *


import json



@login_required
def lista_servicios(requets):

    lista_servicios = Servicios.objects.filter(tienda=requets.user.perfil.tienda.id).order_by('-id')
    total_servicios = lista_servicios.count()
    context = {
        'lista_servicios':lista_servicios,
        'total_servicios':total_servicios,
    }
    return render(requets, 'lista_servicios.html',context)



@login_required
def detalle_servicio(request, servicio_id):
    '''Información detallada del servicio'''

    servicio = Servicios.objects.get(pk=servicio_id)
    
    context = {
        'servicio':servicio
    }
    return render(request, 'detalle_servicio.html', context)


@login_required
def crear_servicio(request, cliente_id):
    '''Creamos un servicio en el sistema'''
    cliente = Cliente.objects.get(pk=cliente_id)
    
    print(cliente)
    if request.method == 'POST':
        print('ingresamos al meth post de crear servicio e imprimimos')
        
        form = ServiciosForm(cliente, request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            if servicio.valor_total > 0:
                servicio.saldo_pendiente = servicio.valor_total
                if servicio.abono > 0:
                    servicio.saldo_pendiente = servicio.saldo_pendiente - servicio.abono
            elif servicio.abono > 0:
                servicio.saldo_pendiente = servicio.saldo_pendiente + servicio.abono
            servicio.estado_orden = Estado_Orden.objects.get(nombre__icontains = 'En Espera de Revisión')
            servicio.tienda = request.user.perfil.tienda
            servicio.save()
            
        return redirect('detalle_servicio', servicio_id=servicio.id)

    else:
        print('ingresamos al form vacio de servicio')
       
        form = ServiciosForm(cliente)
    return render(request, 'servicio_form.html', {'form':form, 'cliente':cliente})
        
    

@login_required
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




@login_required
def eliminar_servicio(request, servicio_id):
    '''Eliminamos un servicio'''

    servicio = Servicios.objects.get(pk=servicio_id)
    servicio.delete()
    return redirect('lista_servicios')



@login_required
def lista_personas(request):
    if 'term' in request.GET:
        q = Cliente.objects.filter(identificacion__icontains = request.GET.get('term')).filter(tienda=request.user.perfil.tienda.id)
        q_n = Cliente.objects.filter(nombres__icontains = request.GET.get('term')).filter(tienda=request.user.perfil.tienda.id)
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


@login_required
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

  

@login_required
def iniciar_trabajo(request, servicio_id):
    servicio = Servicios.objects.get(pk=servicio_id)
    if request.method == 'POST':
        form = IniciarTrabajoForm(request.POST, instance=servicio)
        if form.is_valid():
            orden = form.save(commit=False)

            # Paso 1: orden ingresada a espera de revision  
            if orden.estado_orden.nombre == 'En Espera de Revisión':
                servicio.saldo_pendiente = (orden.valor_total - orden.abono)
                orden.save()
                servicio.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)

            
            # Paso 2: En Espera de Confirmación de Reparación
            elif orden.estado_orden.nombre == 'En Espera de Confirmación de Reparación':
                if orden.valor_total == servicio.valor_total:
                    if orden.abono == servicio.abono:
                        servicio.saldo_pendiente = (orden.valor_total - orden.abono)
                    else:
                        servicio.saldo_pendiente = (orden.valor_total - orden.abono)
                else:
                    if orden.abono == servicio.abono:
                        servicio.saldo_pendiente = (orden.valor_total - orden.abono)
                    else:
                        servicio.saldo_pendiente = (orden.valor_total - orden.abono)
                orden.save()
                servicio.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)
           

            # Paso 3: orden cancelada, ingresa a espera de entrega al cliente, se cobra revision
            elif orden.estado_orden.nombre == 'Orden cancelada, espera entregar equipo al cliente':
                servicio.saldo_pendiente = servicio.valor_revision
                servicio.solucion_final = 'El cliente decidió no reparar el equipo, a espera de que recojan el equipo'
                servicio.fecha_cierre_servicio = datetime.today()
                orden.save()
                servicio.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)
                
                
            # Paso 4: orden cancelada y entregada al cliente
            elif orden.estado_orden.nombre == 'Orden cancelada, equipo entregado al cliente':
                if orden.abono < orden.valor_total:
                    messages.warning(request, 'No se puede cerrar la orden de servicio con saldo pendiente por pagar...') 
                    return render(request, 'iniciar_trabajo.html',{'form':form})
                else:
                    servicio.solucion_final = 'El cliente decidió no reparar el equipo, equipo entregado al cliente'
                    servicio.fecha_cierre_servicio = datetime.today()
                    servicio.saldo_pendiente = (servicio.saldo_pendiente - (orden.abono))
                    orden.save()
                    servicio.save()
                    return redirect('detalle_servicio', servicio_id=servicio.id)

            # Paso 5 Orden aprobada para reparación
            elif orden.estado_orden.nombre == 'Orden aprobada para reparación':
                servicio.saldo_pendiente = orden.valor_total - orden.abono
                servicio.save()
                orden.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)


            # Paso 6: Orden a la espera de repuestos
            elif orden.estado_orden.nombre == 'Orden a la espera de repuestos':
                servicio.saldo_pendiente = orden.valor_total - orden.abono
                orden.save()
                servicio.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)

            # Paso 7: Orden reparada, espera entrega al cliente
            elif orden.estado_orden.nombre == 'Orden reparada, espera entrega al cliente':
                servicio.saldo_pendiente = orden.valor_total - orden.abono
                servicio.fecha_cierre_servicio = datetime.today()
                servicio.save()
                orden.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)

            # Paso 8: Orden reparada, entregada al cliente
            elif orden.estado_orden.nombre == 'Orden reparada, entregada al cliente':
                if orden.abono < orden.valor_total:
                    messages.warning(request, 'No se puede cerrar la orden de servicio con saldo pendiente por pagar...') 
                    return render(request, 'iniciar_trabajo.html',{'form':form})
                else:
                    servicio.saldo_pendiente = orden.valor_total - orden.abono
                    servicio.fecha_cierre_servicio = datetime.today()
                orden.save()
                servicio.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)


            # Paso 9: Orden no reparada, espera entrega al cliente
            elif orden.estado_orden.nombre == 'Orden no reparada, espera entrega al cliente':
                servicio.saldo_pendiente = orden.valor_total - orden.abono
                servicio.fecha_cierre_servicio = datetime.today()
                servicio.solucion_final = 'El equipo no se puede reparar, equipo a la espera de ser reclamado por el cliente.'
                servicio.save()
                orden.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)

            # Paso 10: 	Orden no reparada, entregada al cliente
            elif orden.estado_orden.nombre == 'Orden no reparada, entregada al cliente':
                if orden.abono < orden.valor_total:
                    messages.warning(request, 'No se puede cerrar la orden de servicio con saldo pendiente por pagar...') 
                    return render(request, 'iniciar_trabajo.html',{'form':form})
                else:
                    servicio.saldo_pendiente = orden.valor_total - orden.abono
                    servicio.fecha_cierre_servicio = datetime.today()
                    servicio.solucion_final = 'El equipo no se puede reparar, equipo entregado al cliente.'
                orden.save()
                servicio.save()
                return redirect('detalle_servicio', servicio_id=servicio.id)      
          
                
    else:
        form = IniciarTrabajoForm(instance=servicio)
    return render(request, 'iniciar_trabajo.html', {'form':form})


@login_required
def ordenes_listas_para_reparar(request):
    lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden aprobada para reparación').filter(tienda=request.user.perfil.tienda.id)
    total_ordenes = lista_ordenes.count()
    nombre_lista = 'Ordenes Listas Para Reparación'
    context = {
        'lista_ordenes':lista_ordenes,
        'total_ordenes':total_ordenes,
        'nombre_lista':nombre_lista,
    }
    return render(request, 'lista_ordenes.html', context)


@login_required
def ordenes_espera_revision(request):
    lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Revisión').filter(tienda=request.user.perfil.tienda.id)
    total_ordenes = lista_ordenes.count()
    nombre_lista = 'Ordenes en espera de revisión'
    context = {
        'lista_ordenes':lista_ordenes,
        'total_ordenes':total_ordenes,
        'nombre_lista':nombre_lista,
    }
    return render(request, 'lista_ordenes.html', context)


@login_required
def ordenes_espera_confirmar_reparaion(request):
       lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Confirmación de Reparación').filter(tienda=request.user.perfil.tienda.id)
       total_ordenes = lista_ordenes.count()
       nombre_lista = 'Ordenes en confirmar reparación'
       context = {
       'lista_ordenes':lista_ordenes,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes.html', context)


@login_required
def ordenes_espera_repuestos(request):
       lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden a la espera de repuestos').filter(tienda=request.user.perfil.tienda.id)
       total_ordenes = lista_ordenes.count()
       nombre_lista = 'Ordenes en espera de repuestos'
       context = {
       'lista_ordenes':lista_ordenes,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes.html', context)


@login_required
def ordenes_listas_entrega(request):
       lista_ordenes_canceladas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, espera entregar equipo al cliente').filter(tienda=request.user.perfil.tienda.id)
       lista_ordenes_no_reparadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, espera entrega al cliente').filter(tienda=request.user.perfil.tienda.id)
       lista_ordenes_reparadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, espera entrega al cliente').filter(tienda=request.user.perfil.tienda.id)
       
       total_ordenes = lista_ordenes_canceladas.count() + lista_ordenes_no_reparadas.count() + lista_ordenes_reparadas.count()
       nombre_lista = 'Ordenes listas para entrega al cliente'
       context = {
       'lista_ordenes_canceladas':lista_ordenes_canceladas,
       'lista_ordenes_no_reparadas':lista_ordenes_no_reparadas,
       'lista_ordenes_reparadas':lista_ordenes_reparadas,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes_entregar.html', context)


@login_required
def ordenes_canceladas(request):
       ordenes_canceladas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, equipo entregado al cliente').filter(tienda=request.user.perfil.tienda.id)
       ordenes_no_reparadas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, entregada al cliente').filter(tienda=request.user.perfil.tienda.id)
       total_ordenes = ordenes_canceladas_entregadas.count() + ordenes_no_reparadas_entregadas.count()
       nombre_lista = 'Ordenes canceladas o no reparadas'
       context = {
       'ordenes_canceladas_entregadas':ordenes_canceladas_entregadas,
       'ordenes_no_reparadas_entregadas':ordenes_no_reparadas_entregadas,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes_canceladas.html', context)


@login_required
def ordenes_reparadas(request):
       lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, entregada al cliente').filter(tienda=request.user.perfil.tienda.id)
       total_ordenes = lista_ordenes.count()
       nombre_lista = 'Ordenes Reparadas'
       context = {
       'lista_ordenes':lista_ordenes,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes.html', context)



