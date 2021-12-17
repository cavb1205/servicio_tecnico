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




def email_cambio_suscripcion(membresia):
    '''Envia un mail al administrador de la tienda cuando se hace un cambio de 
    suscripcion para su respectivo pago.'''

    template = get_template('email_cambio_suscripcion.html')
    context = {
        'tienda':membresia,
        }
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Actualización suscripción en PhoneFixSystem',
        '',
        settings.EMAIL_HOST_USER,
        [membresia.tienda.administrador.email],
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    return print('email enviado')


def enviar_email_tienda(tienda, administrador, membresia):
    '''Envia un email al administrador de la tienda con info del registro'''

    template = get_template('email_tienda.html')
    context = {
        'tienda':tienda,
        'administrador':administrador,
        'membresia':membresia,
    }
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Tienda creada en PhoneFixSystem',
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
            membresia = Tienda_membresia.objects.create(tienda=tienda, membresia=Membresia.objects.get(nombre='Gratis'), fecha_activacion=date.today(),fecha_vencimiento=(date.today() + timedelta(days=15)))
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
    if request.method == 'POST':
        form = TiendaForm(request.POST, instance=tienda)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tienda actualizada con éxito.')
            return redirect('perfil_tienda_detalle', tienda.id)
    else:
        print('ingresa al else de editar tienda')
        form = TiendaForm(instance=tienda)
        
    return render(request, 'editar_tienda_form.html',{'form':form})

@login_required
def editar_suscripcion(request, tienda_id):
    '''Editamos la suscripcion con los cambios de dias y pagos pendientes'''

    tienda = Tienda.objects.get(id=tienda_id)
    membresia = Tienda_membresia.objects.get(tienda=tienda)
    if request.method == 'POST':
        form = MembresiaForm(request.POST, instance=membresia)
        if form.is_valid():
            membresia = form.save(commit=False)
            membresia.fecha_activacion = date.today()
            if membresia.membresia.nombre == 'Mensual':
                membresia.fecha_vencimiento = membresia.fecha_activacion + timedelta(days=31)
                membresia.estado = 'Pendiente Pago'
            elif membresia.membresia.nombre == 'Anual':
                membresia.fecha_vencimiento = membresia.fecha_activacion + timedelta(days=365)
                membresia.estado = 'Pendiente Pago'
            membresia.save()
            email_cambio_suscripcion(membresia)
            messages.success(request, 'Suscripción actualizada con éxito.')
            return redirect('perfil_tienda_detalle', tienda.id)
    else:
        form = MembresiaForm(instance=membresia)
    return render(request, 'editar_suscripcion.html',{'form':form})


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


    


##################################################
### vistas de administracion de phonefixsystem ###
##################################################

@login_required
def lista_tiendas(request):
    '''lista todas las tiendas creadas en el sistema'''
    lista_tiendas = Tienda.objects.all()
    total = lista_tiendas.count()
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)

@login_required
def lista_tiendas_inactivas(request):
    '''lista las tiendas inactivas en el sistema'''

    lista_tiendas = Tienda.objects.filter(estado=False)
    total = lista_tiendas.count()

    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)


@login_required
def lista_tiendas_activas(request):
    '''lista las tiendas con suscripcion activa en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__estado='Activa')
    total = lista_tiendas.count()
    
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)


@login_required
def lista_tiendas_vencidas(request):
    '''lista las tiendas con suscripcion vencida en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__estado='Vencida')
    total = lista_tiendas.count()
    
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)


@login_required
def lista_tiendas_pendientes(request):
    '''lista las tiendas con suscripcion pendientes de pago en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__estado='Pendiente Pago')
    total = lista_tiendas.count()
    
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)


@login_required
def lista_tiendas_por_vencer(request):
    '''lista las tiendas con suscripcion proxima a vencer (3 dias) en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__estado='Activa')
    hoy = date.today()
    lista_tiendas = []
    for tienda in lista_tiendas:
        if hoy >= (tienda.fecha_vencimiento - timedelta(days=3)) and tienda.tienda_membresia.estado == 'Activa':
            lista_tiendas.append(tienda)
        else:
            pass

    total = len(lista_tiendas)
    
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)

def lista_tiendas_por_vencer_dashboard():
    '''lista las tiendas con suscripcion proxima a vencer (3 dias) en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__estado='Activa')
    hoy = date.today()
    lista_tiendas = []
    for tienda in lista_tiendas:
        if hoy >= (tienda.fecha_vencimiento - timedelta(days=3)) and tienda.tienda_membresia.estado == 'Activa':
            lista_tiendas.append(tienda)
        else:
            pass
    
    return lista_tiendas

@login_required
def lista_tiendas_suscripcion_gratuita(request):
    '''lista las tiendas con suscripcion gratuita en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__membresia__nombre='Gratis')
    total = lista_tiendas.count()
    print(lista_tiendas)
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)


@login_required
def lista_tiendas_suscripcion_mensual(request):
    '''lista las tiendas con suscripcion mensual en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__membresia__nombre='Mensual')
    total = lista_tiendas.count()
    
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)


@login_required
def lista_tiendas_suscripcion_anual(request):
    '''lista las tiendas con suscripcion anual en el sistema'''
    
    lista_tiendas = Tienda.objects.filter(tienda_membresia__membresia__nombre='Anual')
    total = lista_tiendas.count()
    
    context = {
        'lista_tiendas':lista_tiendas,
        'total':total,
    }
    return render(request,'lista_tiendas.html', context)




@login_required
def admin_dashboard(request):
    '''dashboard para el administrador del sistema donde ve resumen de todas las tiendas'''
    
    
    
    #tiendas#
    lista_tiendas = Tienda.objects.all()
    total_lista_tiendas = lista_tiendas.count()

    lista_tiendas_activas = Tienda.objects.filter(tienda_membresia__estado='Activa')
    total_lista_tiendas_activas = lista_tiendas_activas.count()

    lista_tiendas_inactivas = Tienda.objects.filter(estado=False)
    total_lista_tiendas_inactivas = lista_tiendas_inactivas.count()
    
    lista_tiendas_vencidas = Tienda.objects.filter(tienda_membresia__estado='Vencida')
    total_lista_tiendas_vencidas = lista_tiendas_vencidas.count()

    lista_tiendas_pendientes_pago = Tienda.objects.filter(tienda_membresia__estado='Pendiente Pago')
    total_lista_tiendas_pendientes_pago = lista_tiendas_pendientes_pago.count()

    lista_tiendas_por_vencer = lista_tiendas_por_vencer_dashboard()
    total_lista_tiendas_por_vencer = len(lista_tiendas_por_vencer)

    lista_tiendas_suscripcion_gratuita = Tienda.objects.filter(tienda_membresia__membresia__nombre='Gratis')
    total_lista_tiendas_suscripcion_gratuita = lista_tiendas_suscripcion_gratuita.count()

    lista_tiendas_suscripcion_mensual = Tienda.objects.filter(tienda_membresia__membresia__nombre='Mensual')
    total_lista_tiendas_suscripcion_mensual = lista_tiendas_suscripcion_mensual.count()

    lista_tiendas_suscripcion_anual = Tienda.objects.filter(tienda_membresia__membresia__nombre='Anual')
    total_lista_tiendas_suscripcion_anual = lista_tiendas_suscripcion_anual.count()


    context = {
        ##listas de tiendas##
        'lista_tiendas':lista_tiendas,
        'lista_tiendas_activas':lista_tiendas_activas,
        'lista_tiendas_inactivas':lista_tiendas_inactivas,
        'lista_tiendas_vencidas':lista_tiendas_vencidas,
        'lista_tiendas_pendientes_pago':lista_tiendas_pendientes_pago,
        'lista_tiendas_por_vencer':lista_tiendas_por_vencer,
        'lista_tiendas_suscripcion_gratuita':lista_tiendas_suscripcion_gratuita,
        'lista_tiendas_suscripcion_mensual':lista_tiendas_suscripcion_mensual,
        'lista_tiendas_suscripcion_anual':lista_tiendas_suscripcion_anual,

        ##totales##
        'total_lista_tiendas':total_lista_tiendas,
        'total_lista_tiendas_activas':total_lista_tiendas_activas,
        'total_lista_tiendas_inactivas':total_lista_tiendas_inactivas,
        'total_lista_tiendas_vencidas':total_lista_tiendas_vencidas,
        'total_lista_tiendas_pendientes_pago':total_lista_tiendas_pendientes_pago,
        'total_lista_tiendas_por_vencer':total_lista_tiendas_por_vencer,
        'total_lista_tiendas_suscripcion_gratuita':total_lista_tiendas_suscripcion_gratuita,
        'total_lista_tiendas_suscripcion_mensual':total_lista_tiendas_suscripcion_mensual,
        'total_lista_tiendas_suscripcion_anual':total_lista_tiendas_suscripcion_anual,
    }
    return render(request,'admin_dashboard.html',context)
