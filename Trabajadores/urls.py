from django.contrib import admin
from django.urls import path

from Trabajadores import views

urlpatterns = [
    path('lista/', views.lista_trabajadores, name='lista_trabajadores'),
    path('<int:trabajador_id>/', views.detalle_trabajador, name='detalle_trabajador'),
    path('nuevo/', views.crear_trabajador, name='crear_trabajador'),
    path('editar/<int:trabajador_id>/', views.editar_trabajador, name='editar_trabajador'),
    path('eliminar/<int:trabajador_id>/', views.eliminar_trabajador, name='eliminar_trabajador'),

    #login urls
    path('login/', views.login_view, name='login'),
    
]