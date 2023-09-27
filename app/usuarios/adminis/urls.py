from django.urls import path

#vistas
from app.usuarios.adminis.views import CrearAdminisView, ListarAdminisView, EditarAdminisView, EliminarAdminisView, VerAdminisView

urlpatterns = [
    path('crearAdmin/', CrearAdminisView.as_view(), name="crear_admin"),
    path('listarAdmin/', ListarAdminisView.as_view(), name='listar_admin'),
    path('editarAdmin/<int:pk>/', EditarAdminisView.as_view(), name='editar_admin'),
    path('eliminarAdmin/<int:pk>/', EliminarAdminisView.as_view(), name='eliminar_admin'),
    path('verAdmin/<int:pk>/', VerAdminisView.as_view(), name='ver_admin'),
]