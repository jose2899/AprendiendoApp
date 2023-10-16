from django.db import models
from app.usuarios.usuario.models import Representante

# Create your models here.
class Servicios(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)

    def __str__(self):
        return self.nombre

class Paquete(models.Model):
    horas = models.PositiveIntegerField(default=1)  # Cambiado a PositiveIntegerField
    servicios = models.ForeignKey('Servicios', on_delete=models.CASCADE)  # Relación con el servicio
    representante = models.ForeignKey(Representante, on_delete=models.CASCADE)
    def __str__(self):
        return f"Paquete de {self.horas} horas para {self.servicios} - Representante: {self.representante}"
