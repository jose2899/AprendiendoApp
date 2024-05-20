from django.contrib import admin
<<<<<<< HEAD
from app.terapiass.models import DiaSemana, Diagnostico, Asistencia, HorarioTerapia

# Register your models here.
admin.site.register(Diagnostico)
admin.site.register(DiaSemana)
admin.site.register(Asistencia)
admin.site.register(HorarioTerapia)
=======
from app.terapiass.models import Terapia, DiaSemana, Diagnostico, Horario, AsignacionFechaTerapia, Asistencia

# Register your models here.
admin.site.register(Terapia)
admin.site.register(Diagnostico)
admin.site.register(DiaSemana)
admin.site.register(Horario)
admin.site.register(AsignacionFechaTerapia)
admin.site.register(Asistencia)
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c
