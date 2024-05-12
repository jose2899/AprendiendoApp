from django.contrib import admin
from app.terapiass.models import Terapia, DiaSemana, Diagnostico, Horario, AsignacionFechaTerapia, Asistencia

# Register your models here.
admin.site.register(Terapia)
admin.site.register(Diagnostico)
admin.site.register(DiaSemana)
admin.site.register(Horario)
admin.site.register(AsignacionFechaTerapia)
admin.site.register(Asistencia)
