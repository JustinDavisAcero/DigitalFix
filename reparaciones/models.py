from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

TIPOS_DISPOSITIVO = [
    ('PC', 'PC de Escritorio'),
    ('NB', 'Notebook'),
    ('CEL', 'Celular'),
    ('CON', 'Consola'),
    ('OTR', 'Otro'),
]

ESTADOS_REPARACION = [
    ('POR', 'Por Reparar'),
    ('ENP', 'En Proceso'),
    ('REP', 'Reparado'),
    ('ENT', 'Entregado'),
]

TIPO_SERVICIO_RETIRO = [
    ('retiro', 'Retiro'),
    ('entrega', 'Entrega'),
]

class Cliente(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Dispositivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='dispositivos')
    tipo_dispositivo = models.CharField(max_length=3, choices=TIPOS_DISPOSITIVO, default='CEL')
    modelo = models.CharField(max_length=100)
    problema = models.TextField()
    estado = models.CharField(max_length=3, choices=ESTADOS_REPARACION, default='POR')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_estimada_entrega = models.DateField(null=True, blank=True)
    costo_estimado = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    numero_orden = models.CharField(max_length=15, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            ultimo = Dispositivo.objects.all().order_by('id').last()
            nuevo_id = (ultimo.id + 1) if ultimo else 1
            self.numero_orden = f"ORD-{nuevo_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero_orden} - {self.modelo} ({self.cliente.nombre})'

class RetiroEntrega(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='retiros')
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=30)
    tipo_servicio = models.CharField(max_length=10, choices=TIPO_SERVICIO_RETIRO)
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    numero_orden = models.CharField(max_length=15, unique=True, blank=True, null=True)
    estado = models.CharField(max_length=50, default='Pendiente')

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            prefix = 'R' if self.tipo_servicio == 'retiro' else 'E'
            ts = int(timezone.now().timestamp()) % 100000
            self.numero_orden = f"{prefix}-{ts}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.tipo_servicio} - {self.numero_orden} ({self.cliente.nombre})'

class CitaDiagnostico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='citas')
    correo = models.EmailField()
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return f'Cita de {self.cliente.nombre} - {self.fecha_hora}'

class Mensaje(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='mensajes')
    asunto = models.CharField(max_length=100)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.cliente.nombre} - {self.asunto}'
    
class DiagnosticoTecnico(models.Model):
    dispositivo = models.OneToOneField(Dispositivo, on_delete=models.CASCADE, related_name='diagnostico')
    descripcion_problema = models.TextField()
    diagnostico = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico de {self.dispositivo.numero_orden}"

class Inventario(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"



# ===============================================================
#   SISTEMA DE NOTIFICACIONES AUTOMÁTICAS DE ESTADO (NO TOCAR)
# ===============================================================
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Dispositivo)
def enviar_notificacion_estado(sender, instance, **kwargs):
    """
    Envía correo al cliente cuando cambia el estado del dispositivo.
    """
    if not instance.cliente or not instance.cliente.correo:
        return

    mensaje = f"""
Hola {instance.cliente.nombre},

El estado de su reparación (Orden #{instance.numero_orden}) ha sido actualizado.

Nuevo estado: {instance.get_estado_display()}

Gracias por preferir nuestro servicio.
"""

    send_mail(
        subject='Actualización de Estado de Reparación',
        message=mensaje,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.cliente.correo],
    )
