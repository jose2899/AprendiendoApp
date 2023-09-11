from django.db import models
from django.contrib.auth.models import User

# Definir los posibles servicios como opciones
SERVICIOS_CHOICES = (
    ('Terapia de Lenguaje', 'Terapia de Lenguaje'),
    ('Terapia Neuropedagógica', 'Terapia Neuropedagógica'),
    ('Nivelación', 'Nivelacion'),
    ('Taller de estimulación temprana', 'Taller de estimulación temprana'),
    ('Estimulación temprana', 'Taller de estimulación temprana'),
    ('Talleres', 'Talleres'),
    ('Estimulacion cognitiva', 'Estimulacion cognitiva'),
    ('Estimulacion de lenguaje', 'Estimulacion de lenguaje'),
    # Agrega más opciones según sea necesario
)

# Create your models here.
class Representante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=7)
    celular = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    cedula = models.CharField(max_length=10)
    servicios = models.CharField(
        max_length=50,
        choices=SERVICIOS_CHOICES,
        default='Terepia de Lenguaje'
    )
    otra_terapia = models.CharField(max_length=50)
    conocido = models.CharField(max_length=100)
    observacion = models.TextField(max_length=500)

    def nombre_completo(self):
        return '{} {}'.format(self.nombre, self.apellido)
    
    def __str__(self):
        return self.nombre_completo()

class Estudiante(models.Model):
    representante = models.ForeignKey(Representante, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    año_educacion = models.PositiveIntegerField()
    institucion_educativa = models.CharField(max_length=100)
    fecha = models.DateField()
    motivo = models.TextField(max_length=500)

    def nombre_completo(self):
        return '{} {}'.format(self.nombre, self.apellido)
    
    def __str__(self):
        return self.nombre_completo()