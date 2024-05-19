from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Adminis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    foto = models.ImageField(upload_to='adminis/', null=True, blank=True)
    celular = models.CharField(max_length=10, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)


    def nombre_completo(self):
        return '{} {}'.format(self.nombre, self.apellido)
    
    def __str__(self):
        return self.nombre_completo()


