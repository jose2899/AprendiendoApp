from django.db import models

# Create your models here.
from app.usuarios.usuario.models import Estudiante

class Evento(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    fecha_registro = models.DateField(auto_now_add=True)
    fecha_termino = models.DateField()
    observacion = models.TextField()

    def __str__(self):
        return self.titulo
