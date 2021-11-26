from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from Clientes.models import Cliente

from django.contrib import messages


@login_required
def lista_dispositivos(request):
    '''Lista todos los dispositivos activos'''
    tienda = request.user.perfil.tienda
    lista_dispositivos = Dispositivo.objects.filter(tienda=tienda)
    total_dispositivos = lista_dispositivos.count()
    context = {
        'lista_dispositivos':lista_dispositivos,
        'total_dispositivos':total_dispositivos,
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
def crear_marca(request):
    if request.method == 'POST':
        form = MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marca agregada con éxito.')
            return redirect('lista_dispositivos')
    else:
        form = MarcaForm()
    return render(request, 'marca_form.html', {'form':form})
        


@login_required
def crear_dispositivo(request, cliente_id):
    '''Creamos un dispositivo en el sistema'''
    print('ingresa al crear dispositivo cliente_id = ', cliente_id )
    cliente = Cliente.objects.get(id=cliente_id)
    print(cliente)
    if request.method == 'POST':
        form = DispositivoForm( request.POST)
        
        if form.is_valid():
            dispositivo = form.save(commit=False)
            dispositivo.tienda = request.user.perfil.tienda
            dispositivo.cliente = cliente
            dispositivo.save()
            print(dispositivo.id)
            return redirect('crear_servicio', cliente_id=cliente.id)

    else:
        form = DispositivoForm()
        print(form)
    return render(request, 'dispositivo_form.html', {'form':form})



@login_required
def crear_dispositivo_individual(request):
    '''Creamos un dispositivo en el sistema'''
    tienda = request.user.perfil.tienda
    if request.method == 'POST':
        form = DispositivoIndividualForm(tienda, request.POST)
        print('antes del valid')
        if form.is_valid():

            dispositivo = form.save(commit=False)
            print('ingresa al valid y es commit false')
            dispositivo.tienda = tienda
            print(dispositivo.id)
            print(dispositivo.cliente)
            dispositivo.save()
            return redirect('detalle_dispositivo', dispositivo_id=dispositivo.id)

    else:
        form = DispositivoIndividualForm(tienda)
        
    return render(request, 'dispositivo_form.html', {'form':form})


@login_required
def editar_dispositivo(request, dispositivo_id):
    tienda = request.user.perfil.tienda

    dispositivo = Dispositivo.objects.get(pk=dispositivo_id)
    if request.method == 'POST':
        form = DispositivoForm(tienda,request.POST, instance=dispositivo)
        if form.is_valid():
            dispositivo = form.save(commit=False)
            dispositivo.save()
            return redirect('detalle_dispositivo', dispositivo_id=dispositivo.id)
    else:
        form = DispositivoForm(tienda,instance=dispositivo)
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
