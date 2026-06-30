from django.urls import path
from . import views

app_name = 'turismo'

urlpatterns = [
    path('', views.lista_paquetes, name='lista_paquetes'),
    path('inicio/', views.lista_paquetes, name='inicio'),
    path('paquetes/', views.lista_paquetes, name='lista_paquetes'),
    path('paquete/<int:pk>/', views.detalle_paquete, name='detalle_paquete'),
    path('reserva/crear/<int:paquete_id>/', views.crear_reserva, name='crear_reserva'),
    path('reserva/<str:codigo>/', views.detalle_reserva, name='detalle_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('reserva/<str:codigo>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),
    path('registro/', views.registro_cliente, name='registro_cliente'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),
]