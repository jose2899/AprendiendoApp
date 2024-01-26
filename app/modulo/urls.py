from django.urls import path

#vistas
from app.modulo.views import detalle_estudiante_tdah, listar_estudiantes_tdah 

app_name = 'app.modulo'

urlpatterns = [
    path('listar_estudiantes_tdah/', listar_estudiantes_tdah, name='listar_estudiantes_tdah'),
    path('detalle_estudiante_tdah/<int:estudiante_id>/', detalle_estudiante_tdah, name='detalle_estudiante_tdah'),
]