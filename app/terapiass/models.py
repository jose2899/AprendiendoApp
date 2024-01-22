from django.db import models

# Create your models here.
# terapias/models.py

from app.usuarios.psicologo.models import Psicologo
from app.servicios.models import Paquete
from django.utils import timezone
from app.usuarios.usuario.models import Estudiante

class Terapia(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    
    def __str__(self):
        return f'Terapia para el paquete {self.paquete}'


class DiaSemana(models.Model):
    nombre = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.nombre
    
class AsignacionPsicologo(models.Model):
    terapia = models.ForeignKey(Terapia, on_delete=models.CASCADE)
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    dia_semana = models.ManyToManyField(DiaSemana)

    def __str__(self):
        # Obtiene los nombres completos de los días de la semana seleccionados
        dias_semana = ', '.join(self.dia_semana.values_list('nombre', flat=True))
        return f'Asignación de {self.psicologo.nombre} para la terapia {self.terapia} los {dias_semana}'
    

class AsignacionEstudiante(models.Model):
    terapia = models.ForeignKey(Terapia, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

    def __str__(self):
        return f'Asignación de {self.estudiante.nombre} a {self.terapia}'
    
class HorarioTerapia(models.Model):
    asignacion_psicologo = models.ForeignKey(AsignacionPsicologo, on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f'{self.asignacion_psicologo.psicologo.nombre} - {self.hora_inicio} - {self.hora_fin}'

class Diagnostico(models.Model):
    nombre_diagnostico = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre_diagnostico