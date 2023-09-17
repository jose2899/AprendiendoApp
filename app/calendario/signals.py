from django.db.models.signals import post_save
from django.dispatch import receiver
from app.usuarios.usuario.models import Estudiante
from app.calendario.models import Evento

@receiver(post_save, sender=Estudiante)
def crear_evento_estudiante(sender, instance, **kwargs):
    Evento.objects.create(
        titulo=f"Terapia de {instance.nombre} {instance.apellido}",
        fecha=instance.fecha,
        estudiante=instance,
        observacion="Fecha de inicio de terapia"
    )
