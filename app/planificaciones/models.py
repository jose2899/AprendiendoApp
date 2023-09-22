from django.db import models
from app.usuarios.usuario.models import Estudiante

# Create your models here.
class Planificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    diagnostico = models.TextField()
    edad_biologica = models.IntegerField()
    edad_cognitiva_lenguaje_verbal = models.IntegerField()
    edad_cognitiva_lenguaje_comprensivo = models.IntegerField()

    def __str__(self):
        return f'Planificación para {self.estudiante.nombre} {self.estudiante.apellido}'


class PlanificacionSemana(models.Model):
    planificacion = models.ForeignKey(Planificacion, on_delete=models.CASCADE)
    numero_semana = models.IntegerField()
    tiempo_previsto = models.CharField(max_length=100)
    objetivo = models.TextField()
    actividad_lenguaje = models.TextField()
    actividad_cognitiva = models.TextField()
    actividad_sensorial = models.TextField()
    actividades_internalizadas = models.TextField()
    actividades_reforzar = models.TextField()

    def __str__(self):
        return f'Semana {self.numero_semana} de la planificación para {self.planificacion.estudiante.nombre} {self.planificacion.estudiante.apellido}'

