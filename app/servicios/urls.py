from django.urls import path

#vistas
from app.servicios.views import ServiciosView
from app.servicios.views import ServiciosRView
from app.servicios.views import ServiciosGView

urlpatterns = [
    path('servicios/', ServiciosView.as_view(), name='servicios'),
    path('serviciosR/', ServiciosRView.as_view(), name='serviciosR'),
    path('serviciosG/', ServiciosGView.as_view(), name='serviciosG'),
]