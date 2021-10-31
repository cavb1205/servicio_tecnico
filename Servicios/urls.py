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

    path('ordenes-listas-reparar/', views.ordenes_listas_para_reparar, name='ordenes_listas_reparar'),
    path('ordenes-espera-revision/', views.ordenes_espera_revision, name='ordenes_espera_revision'),
    path('ordenes-confir-reparacion/', views.ordenes_espera_confirmar_reparaion, name='ordenes_espera_confirmar_reparacion'),
    path('ordenes-espera-repuestos/', views.ordenes_espera_repuestos, name='ordenes_espera_repuestos'),
    path('ordenes-listas-entrega/', views.ordenes_listas_entrega, name='ordenes_listas_entrega'),
    path('ordenes-canceladas/', views.ordenes_canceladas, name='ordenes_canceladas'),
    path('ordenes-reparadas/', views.ordenes_reparadas, name='ordenes_reparadas'),

    
]