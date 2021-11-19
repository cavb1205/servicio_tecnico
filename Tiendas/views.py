from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from Tiendas.forms import AdminTiendaForm, TiendaForm
from Tiendas.models import *
from datetime import date
from Trabajadores.models import Perfil




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

        