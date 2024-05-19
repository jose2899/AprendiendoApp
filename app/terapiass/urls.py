# terapias/urls.py
from django.urls import path
from app.terapiass.views import CrearHorarioView
urlpatterns = [
    path('crear_horario/<int:paquete_id>/', CrearHorarioView.as_view(), name='crear_horario'),   
    #path('agregar_psicologo/<int:terapia_id>/', agregar_psicologo, name='agregar_psicologo'),
    #path('detalle_paquete/<int:estudiante_id>/', detalle_paquete, name='detalle_paquete' ),
    #path('informacion_general/<int:estudiante_id>/', informacion_general, name='informacion_general'),
    #path('registrar_asistencia/', registrar_asistencia, name='registrar_asistencia'),

]
