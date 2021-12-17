"""servicio_tecnico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from Trabajadores.views import login_view, logout_view
from Tiendas import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tiendas/', include('Tiendas.urls')),
    path('clientes/', include('Clientes.urls')),
    path('trabajadores/', include('Trabajadores.urls')),
    path('dispositivo/', include('Dispositivos.urls')),
    path('servicios/', include('Servicios.urls')),

    ###vistas del administrador###
    path('administrador/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('administrador/tiendas/', views.lista_tiendas, name='lista_tiendas'),
    path('administrador/tiendas/activas/', views.lista_tiendas_activas, name='lista_tiendas_activas'),
    path('administrador/tiendas/inactivas/', views.lista_tiendas_inactivas, name='lista_tiendas_inactivas'),
    path('administrador/tiendas/vencidas/', views.lista_tiendas_vencidas, name='lista_tiendas_vencidas'),
    path('administrador/tiendas/pendientes/', views.lista_tiendas_pendientes, name='lista_tiendas_pendientes'),    
    path('administrador/tiendas/por/vencer/', views.lista_tiendas_por_vencer, name='lista_tiendas_por_vencer'),
    path('administrador/tiendas/suscripcion/gratuita/', views.lista_tiendas_suscripcion_gratuita, name='lista_tiendas_suscripcion_gratuita'),
    path('administrador/tiendas/suscripcion/mensual/', views.lista_tiendas_suscripcion_mensual, name='lista_tiendas_suscripcion_mensual'),
    path('administrador/tiendas/suscripcion/anual/', views.lista_tiendas_suscripcion_anual, name='lista_tiendas_suscripcion_anual'),
    ################################

    path('', login_view, name='inicio'),

    #login urls appp trabajadores
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

