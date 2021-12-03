from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from Tiendas.forms import AdminTiendaForm, MembresiaForm, TiendaForm
from Tiendas.models import *
from datetime import date, datetime, timedelta
from Trabajadores.models import Perfil
from Servicios.models import Servicios
from Clientes.models import *

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def enviar_email_tienda(tienda, administrador, membresia):
    print('ingresa a funcion enviar email')
    template = get_template('email_tienda.html')
    context = {
        'tienda':tienda,
        'administrador':administrador,
        'membresia':membresia,
    }
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Tienda creada en phonefixsystem',
        '',
        settings.EMAIL_HOST_USER,
        [administrador.email],
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    return print('email enviado con exito')

def crear_tienda(request):
    if request.method == 'POST':
        adminform = AdminTiendaForm(request.POST)
        tiendaform = TiendaForm(request.POST)
        if tiendaform.is_valid() and adminform.is_valid():
            
            administrador = adminform.save(commit=False)
            administrador.username = administrador.email
            administrador.password = make_password(request.POST.get('password'))
            administrador.is_staff = True
            administrador.save()
        
            tienda = tiendaform.save(commit=False)
            tienda.fecha_registro = date.today()
            tienda.administrador = administrador
            tienda.save()

            perfil = Perfil.objects.create(trabajador=administrador, identificacion='n/a', biografia='Administrador Tienda', telefono=tienda.telefono, tienda=tienda)
            membresia = Tienda_membresia.objects.create(tienda=tienda, fecha_activacion=date.today(),fecha_vencimiento=(date.today() + timedelta(days=15)))
            enviar_email_tienda(tienda,administrador, membresia)
            messages.success(request, 'Su cuenta ha sido creada con éxito, por favor inicia sesión en el sistema')
            return redirect('login')
    else:
        adminform = AdminTiendaForm()
        tiendaform = TiendaForm()
        context = {
            'adminform':adminform,
            'tiendaform':tiendaform,
        }
    return render(request, 'tienda_form.html', context)



@login_required
def editar_tienda(request, tienda_id):
    tienda = Tienda.objects.get(id=tienda_id)
    membresia = Tienda_membresia.objects.get(tienda=tienda_id)
    print('consulto la tienda y la membresia')
    print(tienda)
    print(membresia)
    if request.method == 'POST':
        form = TiendaForm(request.POST, instance=tienda)
        membresiaform = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid() and membresiaform.is_valid():
            form.save()
            membresia = membresiaform.save(commit=False)
            membresia.fecha_activacion = date.today()
            if membresia.membresia.nombre == 'Mensual':
                membresia.fecha_vencimiento = membresia.fecha_activacion + timedelta(days=31)
            elif membresia.membresia.nombre == 'Anual':
                membresia.fecha_vencimiento = membresia.fecha_activacion + timedelta(days=365)
            else:
                pass
            membresia.save()
            messages.success(request, 'Tienda actualizada con éxito.')
            return redirect('perfil_tienda_detalle', tienda.id)

    else:
        print('ingresa al else de editar tienda')
        form = TiendaForm(instance=tienda)
        membresiaform = MembresiaForm(instance=membresia)
    return render(request, 'editar_tienda_form.html',{'form':form,'membresiaform':membresiaform})



@login_required
def perfil(request):
    tienda_id = request.user.perfil.tienda.id
    return redirect('perfil_tienda_detalle', tienda_id)

@login_required
def perfil_tienda(request, tienda_id):
    tienda = Tienda.objects.get(id=request.user.perfil.tienda.id)
    context = {
        'tienda':tienda,
    }
    return render(request, 'perfil_tienda.html', context)


@login_required        
def tienda(request):
    usuario = request.user
    tienda = usuario.perfil.tienda
    print('imprimimos usuario y tienda')
    return redirect('detalle_tienda', tienda.id)
    

@login_required
def detalle_tienda(request, tienda_id ):

    tienda = Tienda.objects.get(id=request.user.perfil.tienda.id)

    ordenes_espera_revision = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Revisión').filter(tienda=tienda_id)
    ordenes_espera_confirmar_reparacion = Servicios.objects.filter(estado_orden__nombre__icontains = 'En Espera de Confirmación de Reparación').filter(tienda=tienda_id)
    ordenes_canceladas_espera_entrega = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, espera entregar equipo al cliente').filter(tienda=tienda_id)
    ordenes_canceladas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden cancelada, equipo entregado al cliente').filter(tienda=tienda_id)
    ordenes_aprobadas_reparacion = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden aprobada para reparación').filter(tienda=tienda_id)
    ordenes_espera_repuestos = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden a la espera de repuestos').filter(tienda=tienda_id)
    ordenes_reparadas_espera_entrega = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, espera entrega al cliente').filter(tienda=tienda_id)
    ordenes_reparadas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden reparada, entregada al cliente').filter(tienda=tienda_id)
    ordenes_no_reparadas_espera_entrega = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, espera entrega al cliente').filter(tienda=tienda_id)
    ordenes_no_reparadas_entregadas = Servicios.objects.filter(estado_orden__nombre__icontains = 'Orden no reparada, entregada al cliente').filter(tienda=tienda_id)
    
    clientes = Cliente.objects.filter(tienda=tienda_id).order_by('-id')

    
    #totales
    total_clientes = clientes.count()
    total_ordenes_servicio = Servicios.objects.filter(tienda=tienda_id).count()
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
    ordenes_pendientes = Servicios.objects.filter(tienda=tienda_id).exclude(estado_orden__nombre__icontains = 'En Espera de Revisión').exclude(estado_orden__nombre__icontains = 'En Espera de Confirmación de Reparación').exclude(estado_orden__nombre__icontains = 'Orden cancelada, equipo entregado al cliente').exclude(estado_orden__nombre__icontains = 'Orden aprobada para reparación').exclude(estado_orden__nombre__icontains = 'Orden a la espera de repuestos').exclude(estado_orden__nombre__icontains = 'Orden reparada, entregada al cliente').exclude(estado_orden__nombre__icontains = 'Orden no reparada, entregada al cliente')
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
        
        'tienda':tienda,

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


    