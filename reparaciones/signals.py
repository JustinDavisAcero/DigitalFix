from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Dispositivo


@receiver(pre_save, sender=Dispositivo)
def enviar_notificacion_estado(sender, instance, **kwargs):
    """
    Envía un correo automáticamente cuando cambia el estado del Dispositivo.
    """

    if not instance.pk:
        # El dispositivo aún no existe en la BD (es nuevo)
        return

    estado_anterior = Dispositivo.objects.get(pk=instance.pk).estado
    nuevo_estado = instance.estado

    if estado_anterior != nuevo_estado:
        asunto = f"Actualización de estado de tu reparación Nº {instance.numero_orden}"
        mensaje = (
            f"Hola {instance.cliente.nombre},\n\n"
            f"El estado de tu dispositivo ({instance.modelo}) ha cambiado.\n\n"
            f"Estado anterior: {instance.get_estado_display()}\n"
            f"Nuevo estado: {dict(instance._meta.get_field('estado').choices).get(nuevo_estado)}\n\n"
            f"Gracias por confiar en DigitalFix."
        )

        send_mail(
            asunto,
            mensaje,
            'DigitalFix <{}>'.format("tu_correo"),
            [instance.cliente.correo],
            fail_silently=False
        )
