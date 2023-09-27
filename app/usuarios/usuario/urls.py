from django.urls import path

#vistas
from app.usuarios.usuario.views import CrearRepresentanteView, CrearEstudianteView, ListarRepresentanteView, ListarEstudianteView, VerRepresentanteView, EditarRepresentanteView, EliminarRepresentanteView, VerEstudianteView, EditarEstudianteView, EliminarEstudianteView

urlpatterns = [
    path('crearRepresentante/', CrearRepresentanteView.as_view(), name='crear_representante'),
    path('crearEstudiante/', CrearEstudianteView.as_view(), name='crear_estudiante'),
    path('listarRepresentantes/', ListarRepresentanteView.as_view(), name='listar_representantes'),
    path('listarEstudiantes/', ListarEstudianteView.as_view(), name='listar_estudiantes'),
    path('verRepresentante/<int:pk>/', VerRepresentanteView.as_view(), name='ver_representantes'),
    path('editarRepresentante/<int:pk>/', EditarRepresentanteView.as_view(), name='editar_representante'),
    path('eliminarRepresentante/<int:pk>/', EliminarRepresentanteView.as_view(), name='eliminar_representante'),
    path('verEstudiante/<int:pk>/', VerEstudianteView.as_view(), name='ver_estudiante'),
    path('editarEstudiante/<int:pk>/', EditarEstudianteView.as_view(), name='editar_estudiante'),
    path('eliminarEstudiante/<int:pk>/', EliminarEstudianteView.as_view(), name='eliminar_estudiante'),

]
