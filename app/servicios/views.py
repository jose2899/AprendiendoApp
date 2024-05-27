from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from app.controlRoles.utils import permission_required_custom
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
    
@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
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
            return redirect('crear_horario', paquete_id = paquete.id)
        return render(request, 'servicios/crear_paquete.html', {'form': form, 'servicio': servicio})

class ListarPaquetesView(View):
    def get(self, request, servicio_id):
        servicio = Servicios.objects.get(pk=servicio_id)
        paquetes = Paquete.objects.filter(servicios=servicio)
        return render(request, 'servicios/lista_paquetes.html', {'servicio': servicio, 'paquetes': paquetes})