from django.urls import path
from django.urls import path
from . import views




urlpatterns = [
    path('lista/', views.lista_servicios, name='lista_servicios'),
    path('<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    path('nuevo/<int:cliente_id>/', views.crear_servicio, name='crear_servicio'),
    path('auto/', views.lista_personas, name='lista_personas'),
    path('c/buscar/', views.buscar_cliente, name='buscar_cliente'),
    path('editar/<int:servicio_id>/', views.editar_servicio, name='editar_servicio'),
   # path('eliminar/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('inicio/<int:servicio_id>/', views.iniciar_trabajo, name='iniciar_trabajo'),
    #path('', views.dashboard, name='dashboard'),
]