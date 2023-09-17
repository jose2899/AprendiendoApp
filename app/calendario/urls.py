from django.urls import path
#vistas

from app.calendario.views import EventoCreateView, EventoUpdateView, EventoListView, EventoDeleteView, ver_calendario, obtener_eventos

urlpatterns = [
    path('crearEvento/', EventoCreateView.as_view(), name='crear_evento'),
    path('editarEvento/<int:pk>/', EventoUpdateView.as_view(), name='editar_evento'),
    path('listarEventos/', EventoListView.as_view(), name='lista_eventos'),
    path('eliminarEventos/', EventoDeleteView.as_view(), name='eliminar_eventos'),
    path('verCalendario/', ver_calendario, name='ver_calendario'),
    path('eventos/', obtener_eventos, name='eventos'),
]
