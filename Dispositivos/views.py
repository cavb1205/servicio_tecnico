from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.


@login_required
def lista_dispositivos(request):
    '''Lista todos los dispositivos activos'''

    lista_dispositivos = Dispositivo.objects.all()
    context = {
        'lista_dispositivos':lista_dispositivos
    }
    return render(request, 'lista_dispositivos.html', context)



@login_required
def detalle_dispositivo(request, dispositivo_id):
    '''Información detallada del dispositivo'''

    dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
    
    context = {
        'dispositivo':dispositivo
    }
    return render(request, 'detalle_dispositivo.html', context)



@login_required
def crear_dispositivo(request, cliente_id):
    '''Creamos un dispositivo en el sistema'''
    cliente = Cliente.objects.get(pk=cliente_id)
    if request.method == 'POST':
        form = DispositivoForm(cliente, request.POST)
        
        if form.is_valid():
            dispositivo = form.save()
            print(dispositivo.id)
            return redirect('crear_servicio', cliente_id=cliente.id)

    else:
        form = DispositivoForm(cliente)
        print(form)
    return render(request, 'dispositivo_form.html', {'form':form})



@login_required
def crear_dispositivo_individual(request):
    '''Creamos un dispositivo en el sistema'''
    
    if request.method == 'POST':
        form = DispositivoIndividualForm(request.POST)
        
        if form.is_valid():
            dispositivo = form.save()
            print(dispositivo.id)
            return redirect('detalle_dispositivo', dispositivo_id=dispositivo.id)

    else:
        form = DispositivoIndividualForm()
        
    return render(request, 'dispositivo_form.html', {'form':form})


@login_required
def editar_dispositivo(request, dispositivo_id):

    dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            dispositivo = form.save(commit=False)
            dispositivo.save()
            return redirect('detalle_dispositivo', dispositivo_id=dispositivo.id)
    else:
        form = DispositivoForm(instance=dispositivo)
        print(form)
    return render(request, 'editar_dispositivo_form.html', {'form':form})




@login_required
def eliminar_dispositivo(request, dispositivo_id):
    '''Eliminamos un dispositivo'''

    dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
    dispositivo.delete()
    return redirect('lista_dispositivos')





#vistas para los colores

@login_required
def crear_color(request):
    '''Creamos un color en el sistema'''
    
    if request.method == 'POST':
        form = Color_DispositivoForm(request.POST)
        
        if form.is_valid():
            color = form.save()
            return redirect('lista_dispositivos')

    else:
        form = Color_DispositivoForm()
       
    return render(request, 'color_form.html', {'form':form})



#vistas modelo_dispositivo

@login_required
def crear_modelo_dispositivo(request):
    '''Creamos un modelo nuevo en el sistema'''
    
    if request.method == 'POST':
        form = Modelo_DispositivoForm(request.POST)
        
        if form.is_valid():
            modelo = form.save()
            return redirect('lista_dispositivos')

    else:
        form = Modelo_DispositivoForm()
       
    return render(request, 'modelo_dispositivo_form.html', {'form':form})
