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
            servicio = form.save(commit=False)
            if servicio.valor_total > 0:
                servicio.saldo_pendiente = servicio.valor_total
                if servicio.abono > 0:
                    servicio.saldo_pendiente = servicio.saldo_pendiente - servicio.abono
            elif servicio.abono > 0:
                servicio.saldo_pendiente = servicio.saldo_pendiente + servicio.abono
            
        servicio.save()
            
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



def ordenes_listas_para_reparar(request):
    lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden aprobada para reparación')
    total_ordenes = lista_ordenes.count()
    nombre_lista = 'Ordenes Listas Para Reparación'
    context = {
        'lista_ordenes':lista_ordenes,
        'total_ordenes':total_ordenes,
        'nombre_lista':nombre_lista,
    }
    return render(request, 'lista_ordenes.html', context)

def ordenes_espera_revision(request):
    lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Revisión')
    total_ordenes = lista_ordenes.count()
    nombre_lista = 'Ordenes en espera de revisión'
    context = {
        'lista_ordenes':lista_ordenes,
        'total_ordenes':total_ordenes,
        'nombre_lista':nombre_lista,
    }
    return render(request, 'lista_ordenes.html', context)


def ordenes_espera_confirmar_reparaion(request):
       lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Confirmación de Reparación')
       total_ordenes = lista_ordenes.count()
       nombre_lista = 'Ordenes en confirmar reparación'
       context = {
       'lista_ordenes':lista_ordenes,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes.html', context)


def ordenes_espera_repuestos(request):
       lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden a la espera de repuestos')
       total_ordenes = lista_ordenes.count()
       nombre_lista = 'Ordenes en espera de repuestos'
       context = {
       'lista_ordenes':lista_ordenes,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes.html', context)


def ordenes_listas_entrega(request):
       lista_ordenes_canceladas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, espera entregar equipo al cliente')
       lista_ordenes_no_reparadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, espera entrega al cliente')
       lista_ordenes_reparadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, espera entrega al cliente')
       
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


def ordenes_canceladas(request):
       ordenes_canceladas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, equipo entregado al cliente')
       ordenes_no_reparadas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, entregada al cliente')
       total_ordenes = ordenes_canceladas_entregadas.count() + ordenes_no_reparadas_entregadas.count()
       nombre_lista = 'Ordenes canceladas o no reparadas'
       context = {
       'ordenes_canceladas_entregadas':ordenes_canceladas_entregadas,
       'ordenes_no_reparadas_entregadas':ordenes_no_reparadas_entregadas,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes_canceladas.html', context)


def ordenes_reparadas(request):
       lista_ordenes = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, entregada al cliente')
       total_ordenes = lista_ordenes.count()
       nombre_lista = 'Ordenes Reparadas'
       context = {
       'lista_ordenes':lista_ordenes,
       'total_ordenes':total_ordenes,
       'nombre_lista':nombre_lista,
           }
       return render(request, 'lista_ordenes.html', context)




def dashboard(request):
    ##consultas de ordenes a la bd
    
    ordenes_espera_revision = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Revisión')
    ordenes_espera_confirmar_reparacion = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Confirmación de Reparación')
    ordenes_canceladas_espera_entrega = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, espera entregar equipo al cliente')
    ordenes_canceladas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, equipo entregado al cliente')
    ordenes_aprobadas_reparacion = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden aprobada para reparación')
    ordenes_espera_repuestos = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden a la espera de repuestos')
    ordenes_reparadas_espera_entrega = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, espera entrega al cliente')
    ordenes_reparadas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, entregada al cliente')
    ordenes_no_reparadas_espera_entrega = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, espera entrega al cliente')
    ordenes_no_reparadas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, entregada al cliente')
    
    clientes = Cliente.objects.all().order_by('-id')

    
    #totales
    total_clientes = clientes.count()
    total_ordenes_servicio = Servicios.objects.all().count()
    total_ordenes_espera_revision = ordenes_espera_revision.count()
    total_ordenes_espera_confirmar_reparacion = ordenes_espera_confirmar_reparacion.count()
    total_ordenes_canceladas_espera_entrega = ordenes_canceladas_espera_entrega.count()
    total_ordenes_canceladas_entregadas = ordenes_canceladas_entregadas.count()
    total_ordenes_aprobadas_reparacion = ordenes_aprobadas_reparacion.count()
    total_ordenes_espera_repuestos = ordenes_espera_repuestos.count()
    total_ordenes_reparadas_espera_entrega = ordenes_reparadas_espera_entrega.count()
    total_ordenes_reparadas_entregadas = ordenes_reparadas_entregadas.count()
    total_ordenes_no_reparadas_espera_entrega = ordenes_no_reparadas_espera_entrega.count()
    total_ordenes_no_reparadas_entregadas = ordenes_no_reparadas_entregadas.count()
    total_ordenes_por_entregar = total_ordenes_no_reparadas_espera_entrega + total_ordenes_reparadas_espera_entrega + total_ordenes_canceladas_espera_entrega
    total_ordenes_canceladas = total_ordenes_canceladas_entregadas + total_ordenes_no_reparadas_entregadas

    #clientes pendientes para entregar equipos
    ordenes_pendientes = Servicios.objects.all().exclude(estado_orden__nombre__icontains = 'En Espera de Revisión').exclude(estado_orden__nombre__icontains = 'En Espera de Confirmación de Reparación').exclude(estado_orden__nombre__icontains = 'Orden cancelada, equipo entregado al cliente').exclude(estado_orden__nombre__icontains = 'Orden aprobada para reparación').exclude(estado_orden__nombre__icontains = 'Orden a la espera de repuestos').exclude(estado_orden__nombre__icontains = 'Orden reparada, entregada al cliente').exclude(estado_orden__nombre__icontains = 'Orden no reparada, entregada al cliente')
    clientes_ordenes_pendientes = []
    for orden in ordenes_pendientes:
        clientes_ordenes_pendientes.append(clientes.get(id=orden.cliente.id))

    total_clientes_ordenes_pendientes = len(clientes_ordenes_pendientes)


    #calcular ingresos del dia
    hoy = datetime.now()
    hoy = hoy.strftime("%y-%m-%d")
    ingresos_hoy = ordenes_reparadas_entregadas.filter(fecha_cierre_servicio__icontains = hoy)
    total_ingresos_dia = 0
    for orden in ingresos_hoy:
        print('ingresa al if')
        total_ingresos_dia = total_ingresos_dia + orden.valor_total
        

    #calcular ingresos de la semana
    semana = datetime.now().isocalendar()[1]
    total_ingresos_semana = 0
    for orden in ordenes_reparadas_entregadas:
        if orden.fecha_cierre_servicio.isocalendar()[1] == semana:
            print('ingresa al if de la semana')
            total_ingresos_semana = total_ingresos_semana + orden.valor_total
            
    #calcula ingresos del mes
    mes = datetime.now()
    mes = mes.strftime("%m")
    total_ingresos_mes = 0
    for orden in ordenes_reparadas_entregadas:
        if orden.fecha_cierre_servicio.strftime("%m") == mes:
            total_ingresos_mes = total_ingresos_mes + orden.valor_total

    #calcular ingresos del año
    ano = datetime.now().strftime("%y")
    total_ingresos_ano = 0
    for orden in ordenes_reparadas_entregadas:
        if orden.fecha_cierre_servicio.strftime('%y') == ano:
            total_ingresos_ano = total_ingresos_ano + orden.valor_total



    context = {
        
        'total_clientes':total_clientes,
        'total_ordenes_servicio':total_ordenes_servicio,
        'total_ordenes_espera_revision':total_ordenes_espera_revision,
        'total_ordenes_espera_confirmar_reparacion':total_ordenes_espera_confirmar_reparacion,
        'total_ordenes_canceladas_espera_entrega':total_ordenes_canceladas_espera_entrega,
        'total_ordenes_canceladas_entregadas':total_ordenes_canceladas_entregadas,
        'total_ordenes_aprobadas_reparacion':total_ordenes_aprobadas_reparacion,
        'total_ordenes_espera_repuestos':total_ordenes_espera_repuestos,
        'total_ordenes_reparadas_espera_entrega':total_ordenes_reparadas_espera_entrega,
        'total_ordenes_reparadas_entregadas':total_ordenes_reparadas_entregadas,
        'total_ordenes_no_reparadas_espera_entrega':total_ordenes_no_reparadas_espera_entrega,
        'total_ordenes_no_reparadas_entregadas':total_ordenes_no_reparadas_entregadas,
        'total_ordenes_por_entregar':total_ordenes_por_entregar,
        'total_ordenes_canceladas':total_ordenes_canceladas,


        'clientes_ordenes_pendientes':clientes_ordenes_pendientes,
        'total_clientes_ordenes_pendientes':total_clientes_ordenes_pendientes,

      

        #ingresos
        'total_ingresos_dia':total_ingresos_dia,
        'total_ingresos_semana':total_ingresos_semana,
        'total_ingresos_mes':total_ingresos_mes,
        'total_ingresos_ano':total_ingresos_ano,



    }

    return render(request,'dashboard.html', context)