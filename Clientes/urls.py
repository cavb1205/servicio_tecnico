from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('lista/', views.lista_clientes, name='lista_clientes'),
    path('<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('nuevo/', views.crear_cliente, name='crear_cliente'),
    path('s/nuevo/', views.crear_cliente_servicio, name='crear_cliente_servicio'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('eliminar/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
]