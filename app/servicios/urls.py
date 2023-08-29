from django.urls import path

#vistas
from app.servicios.views import ServiciosView

urlpatterns = [
    path('servicios/', ServiciosView.as_view(), name='servicios')
]