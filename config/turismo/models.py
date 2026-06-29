from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Cliente(models.Model):
    TIPO_DOCUMENTO = [
        ('DNI', 'DNI'),
        ('CE', 'Carné de Extranjería'),
        ('PAS', 'Pasaporte'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO, default='DNI')
    numero_documento = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class PaqueteTuristico(models.Model):
    CATEGORIAS = [
        ('AVENTURA', 'Aventura'),
        ('CULTURAL', 'Cultural'),
        ('NATURALEZA', 'Naturaleza'),
        ('GASTRONOMICO', 'Gastronómico'),
        ('RELIGIOSO', 'Religioso'),
        ('TODO_INCLUIDO', 'Todo Incluido'),
    ]

    DIFICULTAD = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD, default='BAJA')
    duracion_dias = models.IntegerField(validators=[MinValueValidator(1)])
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad_maxima = models.IntegerField(validators=[MinValueValidator(1)])
    incluye = models.TextField()
    no_incluye = models.TextField(blank=True)
    requisitos = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='paquetes/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Paquete Turístico"
        verbose_name_plural = "Paquetes Turísticos"


class Reserva(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    paquete = models.ForeignKey(PaqueteTuristico, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_viaje = models.DateField()
    numero_personas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.cliente.nombres}"

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva']
