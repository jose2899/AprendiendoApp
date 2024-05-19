from django.contrib import admin
from app.terapiass.models import DiaSemana, Diagnostico, Asistencia, HorarioTerapia

# Register your models here.
admin.site.register(Diagnostico)
admin.site.register(DiaSemana)
admin.site.register(Asistencia)
admin.site.register(HorarioTerapia)
