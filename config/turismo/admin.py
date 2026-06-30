from django.contrib import admin
from .models import Cliente, PaqueteTuristico, Itinerario, ServicioAdicional, Reserva, Pago

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'numero_documento', 'telefono', 'email']
    search_fields = ['nombres', 'apellidos', 'numero_documento', 'email']
    list_filter = ['tipo_documento', 'fecha_registro']

@admin.register(PaqueteTuristico)
class PaqueteTuristicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'duracion_dias', 'precio_por_persona', 'cupos_disponibles', 'activo']
    search_fields = ['nombre', 'descripcion']
    list_filter = ['categoria', 'dificultad', 'activo']

@admin.register(Itinerario)
class ItinerarioAdmin(admin.ModelAdmin):
    list_display = ['paquete', 'dia', 'titulo', 'lugar']
    list_filter = ['paquete', 'dia']
    search_fields = ['titulo', 'descripcion']

@admin.register(ServicioAdicional)
class ServicioAdicionalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'costo_adicional']
    list_filter = ['tipo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['codigo_reserva', 'cliente', 'paquete', 'fecha_inicio', 'numero_personas', 'estado']
    list_filter = ['estado', 'metodo_pago', 'fecha_reserva']
    search_fields = ['codigo_reserva', 'cliente__nombres', 'cliente__apellidos']
    readonly_fields = ['codigo_reserva', 'fecha_reserva']

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'reserva', 'monto', 'metodo_pago', 'estado', 'fecha_pago']
    list_filter = ['estado', 'metodo_pago', 'fecha_pago']
    search_fields = ['reserva__codigo_reserva', 'codigo_transaccion']