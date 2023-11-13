from django.contrib import admin
from app.terapiass.models import Terapia, AsignacionEstudiante, AsignacionPsicologo, DiaSemana, HorarioTerapia

# Register your models here.
admin.site.register(Terapia)
admin.site.register(AsignacionEstudiante)
admin.site.register(AsignacionPsicologo)
admin.site.register(DiaSemana)
admin.site.register(HorarioTerapia)