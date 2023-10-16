from django.db import models

# Create your models here.
# terapias/models.py
from django.db import models
from app.usuarios.psicologo.models import Psicologo
from app.servicios.models import Paquete
from app.usuarios.usuario.models import Estudiante
DIAS_SEMANA_CHOICES = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
class Terapia(models.Model):
   
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=50)
    fecha_inicio = models.DateField()

    def __str__(self):
        return f'Terapia con {self.psicologo.nombre} para el paquete {self.paquete} los {self.dia_semana}'

class AsignacionPsicologo(models.Model):
    terapia = models.ForeignKey(Terapia, on_delete=models.CASCADE)
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=20, choices=DIAS_SEMANA_CHOICES)

    def __str__(self):
        return f'Asignación de {self.psicologo.nombre} para la terapia {self.terapia} los {self.dia_semana}'

class AsignacionEstudiante(models.Model):
    terapia = models.ForeignKey(Terapia, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)

    def __str__(self):
        return f'Asignación de {self.estudiante.nombre} a {self.terapia}'
