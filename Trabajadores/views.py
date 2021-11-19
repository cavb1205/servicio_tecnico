from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Servicios.models import Servicios
from Trabajadores.models import Perfil
from .forms import TrabajadorForm, PerfilForm, LoginForm
from django.contrib import messages


from django.contrib.auth import authenticate, login, logout


def login_view(request):
    mensaje = ''
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            #form = LoginForm(request.POST)
            print('ingresa a method post')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print('ingresa al sistema el usuario')
                return redirect('dashboard')
                
            else:
                messages.warning(request, 'El usuario no existe o no se encuentra activo, por favor verifica los datos de ingreso')
                return render(request, 'login.html')
            
        
            
        return render(request, 'login.html')



def lista_trabajadores(request):
    lista_trabajadores = User.objects.all().exclude(is_staff=True).order_by('-is_active')
    total_trabajadores = lista_trabajadores.count()
    for x in lista_trabajadores:
        print(x.groups.all())
    context = {
        'lista_trabajadores':lista_trabajadores,
        'total_trabajadores':total_trabajadores,
    }
    return render(request, 'trabajadores.html', context)


def detalle_trabajador(request, trabajador_id):
    trabajador = User.objects.get(id=trabajador_id)
    servicios = Servicios.objects.filter(tecnico = trabajador.id).order_by('-id')
    context = {
        'trabajador':trabajador,
        'servicios':servicios,
    }
    return render(request, 'detalle_trabajador.html', context)


def crear_trabajador(request):
    if request.method == 'POST':
        userform = TrabajadorForm(request.POST)
        perfilform = PerfilForm(request.POST)
        if userform.is_valid() and perfilform.is_valid():
            p = perfilform.save(commit=False)
            usuario = userform.save()
            perfil = Perfil.objects.create(trabajador=usuario, identificacion = p.identificacion, biografia = p.biografia, telefono = p.telefono)
            usuario.save()
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


def editar_trabajador(request, trabajador_id):
    trabajador = User.objects.get(id=trabajador_id)
    perfil = Perfil.objects.get(trabajador=trabajador.id)

    if request.method == 'POST':
        userform = TrabajadorForm(request.POST, instance=trabajador)
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
        userform = TrabajadorForm(instance=trabajador)
        perfilform = PerfilForm(instance=perfil)
    return render(request, 'trabajador_form.html', {'userform':userform,'perfilform':perfilform})



def eliminar_trabajador(request,trabajador_id):
    trabajador = User.objects.get(id=trabajador_id)
    perfil = Perfil.objects.filter(trabajador=trabajador.id)
    trabajador.delete()
    if perfil != None:
        perfil.delete()
    
    return redirect('lista_trabajadores')