from django.contrib import admin
from django.urls import path

from Tiendas.views import *


urlpatterns = [
    
    path('nuevo/', crear_tienda, name='crear_tienda'),
    path('editar/<int:tienda_id>/', editar_tienda, name='editar_tienda'),
    path('editar/suscripcion/<int:tienda_id>/', editar_suscripcion, name='editar_suscripcion'),
    path('<int:tienda_id>/', detalle_tienda, name='detalle_tienda'),
    path('perfil/', perfil, name='perfil_tienda'),
    path('<int:tienda_id>/perfil/', perfil_tienda, name='perfil_tienda_detalle'),

    path('tienda/', tienda, name='dashboard'),
    
    

    
    
]