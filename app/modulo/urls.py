from django.urls import path

#vistas
from app.modulo.views import detalle_estudiante_tdah
from django.views.generic import TemplateView

urlpatterns = [
    path('progreso_fases/', detalle_estudiante_tdah, name='listar_estudiantes_tdah'),
    path('progreso_fases/<int:estudiante_id>/', detalle_estudiante_tdah, name='detalle_estudiante_tdah'),
]