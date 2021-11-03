from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def lista_trabajadores(request):
    lista_trabajadores = User.objects.all()
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
    context = {
        'trabajador':trabajador,
    }
    return render(request, 'detalle_trabajador.html', context)