from django.urls import path

#vistas
from app.modulo.views import seleccionar_estudiante, transformar_datosF, cargar_modelo, realizar_prediccion
from django.views.generic import TemplateView

urlpatterns = [
    path('progreso_fases/', seleccionar_estudiante, name='listar_estudiantes_tdah'),
    path('progreso_fases/<int:estudiante_id>/transformar_datos/', transformar_datosF, name='transformar_datosF'),
    path('progreso_fases/<int:estudiante_id>/cargar_modelo/', cargar_modelo, name='cargar_modelo'),
    path('progreso_fases/<int:estudiante_id>/realizar_prediccion/', realizar_prediccion, name='realizar_prediccion'),
]