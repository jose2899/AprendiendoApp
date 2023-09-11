from django.urls import path

#vistas
from app.usuarios.usuario.views import CrearRepresentanteView, CrearEstudianteView, ListarRepresentanteView, ListarEstudianteView, VerRepresentanteView

urlpatterns = [
    path('crearRepresentante/', CrearRepresentanteView.as_view(), name='crear_representante'),
    path('crearEstudiante/', CrearEstudianteView.as_view(), name='crear_estudiante'),
    path('listarRepresentantes/', ListarRepresentanteView.as_view(), name='listar_representantes'),
    path('listarEstudiantes/', ListarEstudianteView.as_view(), name='listar_estudiantes'),
    path('verRepresentante/<int:pk>/', VerRepresentanteView.as_view(), name='ver_representantes'),
]