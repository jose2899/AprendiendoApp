from django.urls import path
#vistas
from app.planificaciones.views import PlanificacionCreateView, PlanificacionDeleteView, PlanificacionListView, PlanificacionUpdateView, VerPlanificacionView, PlanificacionSemanaCreateView, PlanificacionSemanaDetailView, PlanificacionSemanaListView, PlanificacionSemanaUpdateView, PlanificacionSemanaDeleteView

urlpatterns = [
    path('crearPlanificacion/', PlanificacionCreateView.as_view(), name='crear_planificacion'),
    path('eliminarPlanificacion/<int:pk>/', PlanificacionDeleteView.as_view(), name='eliminar_planificacion'),
    path('listarPlanificacion/', PlanificacionListView.as_view(), name='listar_planificacion'),
    path('editarPlanificacion/<int:pk>/', PlanificacionUpdateView.as_view(), name='editar_planificacion'),
    path('verPlanificacion/<int:pk>/', VerPlanificacionView.as_view(), name='ver_planificacion'),
    path('crearPSemana/', PlanificacionSemanaCreateView.as_view(), name='crear_p_semana'),
    path('verPSemana/<int:pk>/<int:pk1>/', PlanificacionSemanaDetailView.as_view(), name='ver_p_semana'),
    path('listarPSemana/<int:pk>/', PlanificacionSemanaListView.as_view(), name='listar_p_semana'),
    path('editarPSemana/<int:pk>/<int:pk1>/', PlanificacionSemanaUpdateView.as_view(), name='editar_p_semana'),
    path('eliminarPSemana/<int:pk>/<int:pk1>/', PlanificacionSemanaDeleteView.as_view(), name='eliminar_p_semana'),
]