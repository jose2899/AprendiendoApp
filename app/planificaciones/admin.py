from django.contrib import admin

# Register your models here.
#models
from app.planificaciones.models import Planificacion
from app.planificaciones.models import PlanificacionSemana
# Register your models here.

admin.site.register(Planificacion)
admin.site.register(PlanificacionSemana)
