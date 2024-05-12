from django.db import models

# Create your models here.
# terapias/models.py

from app.usuarios.psicologo.models import Psicologo
from app.servicios.models import Paquete
from django.utils import timezone
from app.usuarios.usuario.models import Estudiante

class DiaSemana(models.Model):
    nombre = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.nombre
    
class Terapia(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    def __str__(self):
        return f'Terapia para el paquete {self.paquete} con el psicologo - {self.psicologo} y con el estudiante - {self.estudiante}'

class Diagnostico(models.Model):
    nombre_diagnostico = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre_diagnostico
    
class Horario(models.Model):
    terapia = models.ForeignKey(Terapia, related_name='horarios', on_delete=models.CASCADE)
    dia_semana = models.ForeignKey(DiaSemana, on_delete=models.CASCADE)
    hora_inicio = models.TimeField()   
    def __str__(self):
        return f'Horario para {self.terapia.psicologo} el {self.dia_semana} a las {self.hora_inicio} para {self.terapia.estudiante}'

class AsignacionFechaTerapia(models.Model):
    terapia = models.ForeignKey(Terapia, related_name='fechaTerapia', on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    # Otros campos si es necesario
    def __str__(self):
        return f'Asignado a la terapia {self.terapia} desde {self.fecha_inicio}'
    
class Asistencia(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha = models.DateField()
    asistio = models.BooleanField(default=False)
    horas_restantes = models.IntegerField()


    def __str__(self):
        return f"Asistencia de {self.estudiante} el {self.fecha}"
    
