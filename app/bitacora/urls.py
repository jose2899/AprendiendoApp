from django.urls import path

#vistas
from app.bitacora.views import CrearBitacoraView, ListarBitacoraView, EditarBitacoraView, VerBitacoraView, EliminarBitacoraView, CrearNuevaBitacoraView, DetalleBitacoraView

urlpatterns = [
    path('listarBitacora/', ListarBitacoraView.as_view(), name='listar_bitacora'),
    path('crearBitacora/', CrearBitacoraView.as_view(), name='crear_bitacora'),
    path('editarBitacora/<int:pk>/', EditarBitacoraView.as_view(), name='editar_bitacora'),
    path('eliminarBitacora/<int:pk>/', EliminarBitacoraView.as_view(), name='eliminar_bitacora'),
    path('verBitacora/<int:pk>/', VerBitacoraView.as_view(), name='ver_bitacora'),
    path('crear_nueva_bitacora/<int:estudiante_id>/', CrearNuevaBitacoraView.as_view(), name='crearNuevaBitacora'),
    path('detalle_bitacora/<int:pk>/', DetalleBitacoraView.as_view(), name='detalleBitacora'),
]
