from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('lista/', views.lista_dispositivos, name='lista_dispositivos'),
    path('<int:dispositivo_id>/', views.detalle_dispositivo, name='detalle_dispositivo'),
    path('nuevo/', views.crear_dispositivo_individual, name='crear_dispositivo_individual'),
    path('nuevo/<int:cliente_id>/', views.crear_dispositivo, name='crear_dispositivo'),
    path('editar/<int:dispositivo_id>/', views.editar_dispositivo, name='editar_dispositivo'),
    path('eliminar/<int:dispositivo_id>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    
    #rutas para colores de dispositivos
    path('color/nuevo/', views.crear_color, name='crear_color'),
    path('marca/nuevo/', views.crear_marca, name='crear_marca'),
    

    path('modelo/nuevo/', views.crear_modelo_dispositivo, name='crear_modelo_dispositivo'),
]