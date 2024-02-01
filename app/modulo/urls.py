from django.urls import path

#vistas
from app.modulo.views import detalle_estudiante_tdah, listar_estudiantes_tdah, predecir_avance_lectoescritura


urlpatterns = [
    path('listar_estudiantes_tdah/', listar_estudiantes_tdah, name='listar_estudiantes_tdah'),
    path('detalle_estudiante_tdah/<int:estudiante_id>/', detalle_estudiante_tdah, name='detalle_estudiante_tdah'),
    path('predecir_avance/<int:estudiante_id>/', predecir_avance_lectoescritura, name='predecir_avance'),
]