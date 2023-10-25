# terapias/urls.py
from django.urls import path
from app.terapiass.views import CrearTerapiaView, AsignarEstudianteView, TerapiaDetailView
urlpatterns = [
    path('crear_terapia/', CrearTerapiaView.as_view(), name='crear_terapia'),
    path('asignar_estudiante', AsignarEstudianteView.as_view(), name='asignar_estudiante'),
    path('terapia/', TerapiaDetailView.as_view(), name='terapia_detail'),
    # ... otras URLs que puedas necesitar
]
