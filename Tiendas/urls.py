from django.contrib import admin
from django.urls import path

from Tiendas.views import *


urlpatterns = [
    
    path('nuevo/', crear_tienda, name='crear_tienda'),
    path('<int:tienda_id>/', detalle_tienda, name='detalle_tienda'),


    path('tienda/', tienda, name='dashboard'),
    
    

    
    
]