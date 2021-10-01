from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('lista/', views.lista_clientes, name='lista_clientes'),
    path('<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
]