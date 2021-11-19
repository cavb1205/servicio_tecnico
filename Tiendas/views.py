from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from Tiendas.forms import AdminTiendaForm, TiendaForm
from Tiendas.models import *
from datetime import date




def crear_tienda(request):
    if request.method == 'POST':
        adminform = AdminTiendaForm(request.POST)
        tiendaform = TiendaForm(request.POST)
        if tiendaform.is_valid() and adminform.is_valid():
            
            administrador = adminform.save(commit=False)
            administrador.username = administrador.email
            administrador.save()
            tienda = tiendaform.save(commit=False)
            tienda.fecha_registro = date.today()
            tienda.administrador = administrador
            tienda.save()
            return redirect('dashboard')
    else:
        adminform = AdminTiendaForm()
        tiendaform = TiendaForm()
        context = {
            'adminform':adminform,
            'tiendaform':tiendaform,
        }
    return render(request, 'tienda_form.html', context)

        