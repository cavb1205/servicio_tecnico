from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.urls import reverse
from Servicios.models import Servicios
from Trabajadores.models import Perfil
from .forms import TrabajadorForm, PerfilForm, PasswordForm, EditarTrabajadorForm

from Tiendas.models import Tienda


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


def login_view(request):
    mensaje = ''
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            
            print('ingresa a method post')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                t = user.perfil.tienda
                tienda = Tienda.objects.get(id=t.id)
                if tienda.estado == True:
                    login(request, user)
                    
                    return redirect('detalle_tienda', tienda_id=t.id )
                else:
                    print('ingresa al else de la tienda desactivada')
                    messages.warning(request, 'La tienda ' + tienda.nombre + ' se encuentra desactivada, por favor contacta a soporte para activarla.')
                    return render(request,'login.html')
            else:
                messages.warning(request, 'El usuario no existe o no se encuentra activo, por favor verifica los datos de ingreso')
                return render(request, 'login.html')
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def lista_trabajadores(request):
    tienda = request.user.perfil.tienda.id
    print(tienda)
    trabajadores = Perfil.objects.filter(tienda=tienda)
    print(trabajadores)
    
    lista_trabajadores = User.objects.filter(perfil__tienda = tienda).exclude(is_staff=True).order_by('-is_active')
    total_trabajadores = lista_trabajadores.count()
    for x in lista_trabajadores:
        print(x.groups.all())
    context = {
        'lista_trabajadores':lista_trabajadores,
        'total_trabajadores':total_trabajadores,
    }
    return render(request, 'trabajadores.html', context)


@login_required
def detalle_trabajador(request, trabajador_id):
    trabajador = User.objects.get(id=trabajador_id)
    servicios = Servicios.objects.filter(tecnico = trabajador.id).order_by('-id')
    context = {
        'trabajador':trabajador,
        'servicios':servicios,
    }
    return render(request, 'detalle_trabajador.html', context)


@login_required
def crear_trabajador(request):
    tienda = request.user.perfil.tienda
    
    if request.method == 'POST':
        userform = TrabajadorForm(request.POST)
        perfilform = PerfilForm(request.POST)
        if userform.is_valid() and perfilform.is_valid():
            p = perfilform.save(commit=False)
            usuario = userform.save(commit=False)
            usuario.username = usuario.email
            usuario.set_password(request.POST.get('password'))
            usuario.save()
            perfil = Perfil.objects.create(trabajador=usuario, identificacion = p.identificacion, biografia = p.biografia, telefono = p.telefono, tienda=tienda)
            perfil.save()
            messages.success(request, 'Trabajador creado con éxito.') 
            return redirect('detalle_trabajador', trabajador_id=usuario.id)
        else:
            messages.warning(request, 'No se pudo crear el registro, por favor corregir los datos.') 
            return render(request,'trabajador_form.html', {'userform':userform,'perfilform':perfilform})
    else:
        userform = TrabajadorForm()
        perfilform = PerfilForm()
    return render(request, 'trabajador_form.html', {'userform':userform,'perfilform':perfilform})


@login_required
def editar_trabajador(request, trabajador_id):
    trabajador = User.objects.get(id=trabajador_id)
    perfil = Perfil.objects.get(trabajador=trabajador.id)

    if request.method == 'POST':
        userform = EditarTrabajadorForm(request.POST, instance=trabajador)
        perfilform = PerfilForm(request.POST, instance=perfil)
        if userform.is_valid() and perfilform.is_valid():
            usuario = userform.save()
            perfilform.save()
            messages.success(request, 'Trabajador modificado con éxito.') 
            return redirect('detalle_trabajador', trabajador_id=usuario.id)
        else:
            messages.warning(request, 'No se pudo crear el registro, por favor corregir los datos.') 
            return render(request,'trabajador_form.html', {'userform':userform,'perfilform':perfilform})
    else:
        userform = EditarTrabajadorForm(instance=trabajador)
        perfilform = PerfilForm(instance=perfil)
    return render(request, 'trabajador_form.html', {'userform':userform,'perfilform':perfilform})



@login_required
def cambiar_password(request, trabajador_id):
    trabajador = User.objects.get(id=trabajador_id)
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():

            trabajador.set_password(request.POST.get('password'))
            trabajador.save()
            messages.success(request, 'Contraseña actualizada con éxito.')
            return redirect('detalle_trabajador', trabajador.id)
        else:
            messages.error(request, 'La contraseña no cumple con las condiciones mínimas.')
            return redirect('detalle_trabajador', trabajador.id)
    else:
        form = PasswordForm()
    return render(request,'password.html',{'form':form})

@login_required
def eliminar_trabajador(request,trabajador_id):
    trabajador = User.objects.get(id=trabajador_id)
    perfil = Perfil.objects.filter(trabajador=trabajador.id)
    trabajador.delete()
    if perfil != None:
        perfil.delete()
    
    return redirect('lista_trabajadores')