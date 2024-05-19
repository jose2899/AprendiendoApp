from django.urls import path

#vistas
from app.usuarios.psicologo.views import CrearPsicologoView, ListarPsicologoView, EditarPsicologoView, EliminarPsicologoView, VerPsicologoView

urlpatterns = [
    path('crearPsicologo/', CrearPsicologoView.as_view(), name="crear_psicologo"),
    path('listarPsicologos/', ListarPsicologoView.as_view(), name='listar_psicologos'),
    path('editarPsicologo/<int:pk>/', EditarPsicologoView.as_view(), name='editar_psicologo'),
    path('eliminarPsicologo/<int:pk>/', EliminarPsicologoView.as_view(), name='eliminar_psicologo'),
    path('verPsicologo/<int:pk>/', VerPsicologoView.as_view(), name='ver_psicologo'),
]