from django.db import models
from app.terapiass.models import HorarioTerapia

# Create your models here.
class Asistencia(models.Model):
    horario= models.ForeignKey(HorarioTerapia, on_delete=models.CASCADE, related_name='asistencias')
    asistencia = models.BooleanField(default=False)  # Campo para registrar la asistencia
    fecha = models.DateField()
    def __str__(self):
        return f"Asistencia de {self.horario.paquete.estudiante} en {self.horario}"