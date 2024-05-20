# terapias/urls.py
from django.urls import path
<<<<<<< HEAD
from app.terapiass.views import CrearHorarioView
urlpatterns = [
    path('crear_horario/<int:paquete_id>/', CrearHorarioView.as_view(), name='crear_horario'),   
    #path('agregar_psicologo/<int:terapia_id>/', agregar_psicologo, name='agregar_psicologo'),
    #path('detalle_paquete/<int:estudiante_id>/', detalle_paquete, name='detalle_paquete' ),
    #path('informacion_general/<int:estudiante_id>/', informacion_general, name='informacion_general'),
    #path('registrar_asistencia/', registrar_asistencia, name='registrar_asistencia'),
=======
from app.terapiass.views import crear_terapia, agregar_psicologo, detalle_paquete, informacion_general, registrar_asistencia
urlpatterns = [
    path('crear_terapia/', crear_terapia, name='crear_terapia'),   
    path('agregar_psicologo/<int:terapia_id>/', agregar_psicologo, name='agregar_psicologo'),
    path('detalle_paquete/<int:estudiante_id>/', detalle_paquete, name='detalle_paquete' ),
    path('informacion_general/<int:estudiante_id>/', informacion_general, name='informacion_general'),
    path('registrar_asistencia/', registrar_asistencia, name='registrar_asistencia'),
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c

]
