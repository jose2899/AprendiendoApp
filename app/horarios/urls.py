from django.urls import path
from app.horarios.views import listar_horarios, RegistrarAsistenciaView, listar_todos_horarios

urlpatterns = [
    path('listarHorarios/', listar_horarios, name='listarHorarios'),
    path('registrarAsistencia/<int:horario_id>/', RegistrarAsistenciaView.as_view(), name='registrarAsistencia'),
    path('listarTodosHorarios/', listar_todos_horarios, name='listarTodosHorarios'),
]