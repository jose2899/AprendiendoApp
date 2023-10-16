# terapias/urls.py
from django.urls import path
from app.terapias.views import CrearTerapiaView, AsignarEstudianteView

urlpatterns = [
    path('crear_terapia/', CrearTerapiaView.as_view(), name='crear_terapia'),
    path('asignar_estudiante/<int:terapia_id>/', AsignarEstudianteView.as_view(), name='asignar_estudiante'),
    # ... otras URLs que puedas necesitar
]
