from django.shortcuts import render

#modelos
from app.servicios.models import Servicios

#vistas
from django.views.generic import ListView

# Create your views here.

class ServiciosView(ListView):
    model = Servicios
    template_name = "servicios/servicios.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = Servicios.objects.all()
        return context