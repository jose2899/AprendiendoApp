# terapias/urls.py
from django.urls import path
from app.terapiass.views import crear_terapia, agregar_psicologo, detalle_paquete, informacion_general, registrar_asistencia
urlpatterns = [
    path('crear_terapia/', crear_terapia, name='crear_terapia'),   
    path('agregar_psicologo/<int:terapia_id>/', agregar_psicologo, name='agregar_psicologo'),
    path('detalle_paquete/<int:estudiante_id>/', detalle_paquete, name='detalle_paquete' ),
    path('informacion_general/<int:estudiante_id>/', informacion_general, name='informacion_general'),
    path('registrar_asistencia/', registrar_asistencia, name='registrar_asistencia'),

]
