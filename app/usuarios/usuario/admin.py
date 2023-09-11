from django.contrib import admin
#models
from app.usuarios.usuario.models import Representante
from app.usuarios.usuario.models import Estudiante

# Register your models here.
admin.site.register(Representante)
admin.site.register(Estudiante)
