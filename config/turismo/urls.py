from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),

    # Página principal
    path('', views.inicio, name='inicio'),
    path('inicio/', views.inicio, name='inicio'),

    # Paquetes
    path('paquetes/', views.lista_paquetes, name='lista_paquetes'),
    path('paquete/<int:pk>/', views.detalle_paquete, name='detalle_paquete'),

    # Reservas
    path('reservar/<int:paquete_id>/', views.crear_reserva, name='crear_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('reserva/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('reserva/<int:reserva_id>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),

    # Reporte
    path('reporte/', views.reporte_reservas, name='reporte_reservas'),

    # Perfil
    path('perfil/', views.perfil_view, name='perfil'),
]
