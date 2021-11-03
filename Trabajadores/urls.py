from django.contrib import admin
from django.urls import path

from Trabajadores import views

urlpatterns = [
    path('lista/', views.lista_trabajadores, name='lista_trabajadores'),
    path('<int:trabajador_id>/', views.detalle_trabajador, name='detalle_trabajador'),
    
]