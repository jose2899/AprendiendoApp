from django.urls import path

#vistas
from app.servicios.views import ServiciosView
from app.servicios.views import ServiciosRView
from app.servicios.views import ServiciosGView, CrearPaqueteView, ListarPaquetesView

urlpatterns = [
    path('servicios/', ServiciosView.as_view(), name='servicios'),
    path('serviciosR/', ServiciosRView.as_view(), name='serviciosR'),
    path('serviciosG/', ServiciosGView.as_view(), name='serviciosG'),
    path('crear_paquete/<int:servicio_id>/', CrearPaqueteView.as_view(), name='crear_paquete'),
    path('lista_paquetes/<int:servicio_id>/', ListarPaquetesView.as_view(), name='lista_paquetes'),

]