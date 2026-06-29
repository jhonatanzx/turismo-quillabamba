from django.contrib import admin
from .models import Cliente, PaqueteTuristico, Reserva

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'numero_documento', 'telefono', 'email']
    search_fields = ['nombres', 'apellidos', 'numero_documento']

@admin.register(PaqueteTuristico)
class PaqueteTuristicoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'duracion_dias', 'precio_por_persona', 'activo']
    list_filter = ['categoria', 'dificultad', 'activo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'paquete', 'fecha_viaje', 'numero_personas', 'precio_total', 'estado']
    list_filter = ['estado', 'fecha_reserva']
    search_fields = ['cliente__nombres', 'cliente__apellidos', 'paquete__nombre']
    readonly_fields = ['fecha_reserva']
