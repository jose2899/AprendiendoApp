from django.urls import path

#vistas
from app.usuarios.adminis.views import CrearAdminisView, ListarAdminisView

urlpatterns = [
    path('crearAdmin/', CrearAdminisView.as_view(), name="crear_admin"),
    path('listarAdmin/', ListarAdminisView.as_view(), name='listar_admin')
]