from django.urls import path

#vistas
from app.horario.views import CrearHorarioView, ListarHorarioView, EliminarHorarioView, EditarHorarioView, VerHorarioView
urlpatterns = [
    path('listarHorario/', ListarHorarioView.as_view(), name='listar_horario'),
<<<<<<< HEAD
    path('crearHorario/', CrearHorarioView.as_view(), name='crearHorario'),
=======
    path('crearHorario/', CrearHorarioView.as_view(), name='crear_horario'),
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c
    path('eliminarHorario/<int:pk>/', EliminarHorarioView.as_view(), name='eliminar_horario'),
    path('editarHorario/<int:pk>/', EditarHorarioView.as_view(), name='editar_horario'),
    path('verHorario/<int:pk>/', VerHorarioView.as_view(), name='ver_horario'),
]