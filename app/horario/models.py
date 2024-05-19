
# Create your models here.
from django.db import models
from app.usuarios.usuario.models import Estudiante
from app.usuarios.psicologo.models import Psicologo
# Create your models here.

class Horario(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE)
    terapia = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dia = models.CharField(max_length=10)
    

    def __str__(self):
        return f'Clase de {self.terapia} para {self.estudiante} a las {self.hora_inicio} a {self.hora_fin} el día {self.dia}'

