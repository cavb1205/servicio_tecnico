from django.contrib import admin
from django.urls import path

from Tiendas.views import crear_tienda

urlpatterns = [
    
    path('nuevo/', crear_tienda, name='crear_tienda'),
    

    
    
]