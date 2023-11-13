# terapias/urls.py
from django.urls import path
from app.terapiass.views import CrearTerapiaView, AsignarEstudianteView,AgregarHorarioTerapiaView
urlpatterns = [
    path('crear_terapia/', CrearTerapiaView.as_view(), name='crear_terapia'),
    path('asignar_estudiante', AsignarEstudianteView.as_view(), name='asignar_estudiante'),
    path('agregar_horario_terapia/<int:terapia_id>/', AgregarHorarioTerapiaView.as_view(), name='agregar_horario_terapia'),
    # ... otras URLs que puedas necesitar
]
