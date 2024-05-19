from django.db import models
from app.planificaciones.models import Planificacion
from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico


# Create your models here.
class Bitacora(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    planificacion = models.ForeignKey(Planificacion, on_delete=models.CASCADE)
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bitácora de la Planificación #{self.planificacion.id}'

ASISTENCIAS_CHOICES = (
    ('si', 'si'),
    ('no','no'),
)

CONDUCTAS_CHOICES = (
    ('excelente', 'excelente'),
    ('buena','buena'),
    ('regular','regular'),
)

AVANCE_CHOICES = (
    ('mejorando', 'mejorando'),
    ('regular','regular'),
    ('retroceso','retroceso'),
)
class NuevaBitacora(models.Model):
    bitacora = models.ForeignKey(Bitacora, on_delete=models.CASCADE)
    fecha = models.DateField()
    observacion_conducta = models.CharField(
        max_length=50,
        choices = CONDUCTAS_CHOICES,
        default='buena')
    temas_trabajados = models.CharField(max_length=400)
    avance = models.CharField(
        max_length=50,
        choices = AVANCE_CHOICES,
        default='regular')
    firma_terapeuta = models.CharField(max_length=100)
    revisado_por = models.CharField(max_length=100)
    asistencias = models.CharField(
        max_length=10,
        choices = ASISTENCIAS_CHOICES,
        default='si'
    )

    def save(self, *args, **kwargs):
        # Asignar la bitacora automáticamente antes de guardar
        if not self.bitacora_id:
            bitacora_id = kwargs.pop('bitacora_id', None)
            if bitacora_id:
                self.bitacora_id = bitacora_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Nueva bitacora de #{self.bitacora.id}'
