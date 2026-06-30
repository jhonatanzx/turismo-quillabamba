from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

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
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.numero_documento}"
    
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
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    precio_por_persona = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad_maxima = models.IntegerField(validators=[MinValueValidator(1)])
    cupos_disponibles = models.IntegerField(validators=[MinValueValidator(0)])
    incluye = models.TextField(help_text="Lista de servicios incluidos")
    no_incluye = models.TextField(help_text="Lista de servicios no incluidos", blank=True)
    requisitos = models.TextField(blank=True, help_text="Requisitos para el tour")
    imagen_principal = models.ImageField(upload_to='paquetes/', null=True, blank=True)
    imagen_banner = models.ImageField(upload_to='paquetes/banners/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.categoria}"
    
    def precio_total(self, num_personas):
        return self.precio_por_persona * num_personas
    
    def cupos_restantes(self):
        reservas_confirmadas = self.reserva_set.filter(estado='CONFIRMADA').count()
        return self.capacidad_maxima - reservas_confirmadas
    
    class Meta:
        verbose_name = "Paquete Turístico"
        verbose_name_plural = "Paquetes Turísticos"
        ordering = ['-fecha_creacion']

class Itinerario(models.Model):
    paquete = models.ForeignKey(PaqueteTuristico, on_delete=models.CASCADE, related_name='itinerarios')
    dia = models.IntegerField(validators=[MinValueValidator(1)])
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    actividades = models.TextField(help_text="Lista de actividades del día")
    lugar = models.CharField(max_length=200)
    
    def __str__(self):
        return f"Día {self.dia}: {self.titulo} - {self.paquete.nombre}"
    
    class Meta:
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerarios"
        ordering = ['dia']

class ServicioAdicional(models.Model):
    TIPO_SERVICIO = [
        ('TRANSPORTE', 'Transporte'),
        ('HOSPEDAJE', 'Hospedaje'),
        ('ALIMENTACION', 'Alimentación'),
        ('GUIA', 'Guía Turístico'),
        ('SEGURO', 'Seguro de Viaje'),
        ('EQUIPO', 'Equipo Especial'),
        ('OTRO', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_SERVICIO)
    descripcion = models.TextField()
    costo_adicional = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    paquetes = models.ManyToManyField(PaqueteTuristico, related_name='servicios_adicionales', blank=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_display()}"
    
    class Meta:
        verbose_name = "Servicio Adicional"
        verbose_name_plural = "Servicios Adicionales"

class Reserva(models.Model):
    ESTADO_RESERVA = [
        ('PENDIENTE', 'Pendiente de Pago'),
        ('CONFIRMADA', 'Confirmada'),
        ('PAGADA', 'Pagada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    
    METODO_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta de Crédito/Débito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('YAPE', 'Yape'),
        ('PLIN', 'Plin'),
    ]
    
    codigo_reserva = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    paquete = models.ForeignKey(PaqueteTuristico, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    numero_personas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_RESERVA, default='PENDIENTE')
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO, null=True, blank=True)
    observaciones = models.TextField(blank=True)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    motivo_cancelacion = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.codigo_reserva} - {self.cliente.nombres} - {self.paquete.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo_reserva:
            import datetime
            fecha = datetime.datetime.now().strftime('%Y%m%d')
            from django.utils.crypto import get_random_string
            codigo = get_random_string(4, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            self.codigo_reserva = f"QLB-{fecha}-{codigo}"
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ['-fecha_reserva']

class Pago(models.Model):
    ESTADO_PAGO = [
        ('PENDIENTE', 'Pendiente'),
        ('COMPLETADO', 'Completado'),
        ('FALLIDO', 'Fallido'),
        ('REEMBOLSADO', 'Reembolsado'),
    ]
    
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=20, choices=Reserva.METODO_PAGO)
    estado = models.CharField(max_length=20, choices=ESTADO_PAGO, default='PENDIENTE')
    comprobante = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    codigo_transaccion = models.CharField(max_length=100, blank=True)
    observaciones = models.TextField(blank=True)
    
    def __str__(self):
        return f"Pago {self.id} - {self.reserva.codigo_reserva} - S/.{self.monto}"
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']