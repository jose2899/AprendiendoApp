from django.shortcuts import render, redirect

#modelos
from app.servicios.models import Servicios
from app.servicios.models import Paquete
from app.usuarios.usuario.models import Representante
from django.views import View

#vistas
from django.views.generic import ListView
from app.servicios.forms import PaqueteForm

# Create your views here.

class ServiciosView(ListView):
    model = Servicios
    template_name = "servicios/servicios.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = Servicios.objects.all()
        return context
    
class ServiciosRView(ListView):
    model = Servicios
    template_name = "servicios/serviciosR.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = Servicios.objects.all()
        return context
    
class ServiciosGView(ListView):
    model = Servicios
    template_name = "servicios/serviciosG.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios'] = Servicios.objects.all()
        return context

class CrearPaqueteView(View):
    def get(self, request, servicio_id):
        servicio = Servicios.objects.get(pk=servicio_id)
        form = PaqueteForm(servicio_id=servicio_id) 
        return render(request, 'servicios/crear_paquete.html', {'form': form, 'servicio': servicio})

    def post(self, request, servicio_id):
        servicio = Servicios.objects.get(pk=servicio_id)
        form = PaqueteForm(request.POST, servicio_id=servicio_id)
        if form.is_valid():
            paquete = form.save(commit=False)
            paquete.servicios = servicio
            paquete.save()
<<<<<<< HEAD
            return redirect('crear_horario', paquete_id = paquete.id)
=======
            return redirect('lista_paquetes', servicio_id=servicio_id)
>>>>>>> 58ca78afafb93ce38d26e19bdf0e79d9c5449f2c
        return render(request, 'servicios/crear_paquete.html', {'form': form, 'servicio': servicio})

class ListarPaquetesView(View):
    def get(self, request, servicio_id):
        servicio = Servicios.objects.get(pk=servicio_id)
        paquetes = Paquete.objects.filter(servicios=servicio)
        return render(request, 'servicios/lista_paquetes.html', {'servicio': servicio, 'paquetes': paquetes})