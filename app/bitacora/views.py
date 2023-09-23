from django.shortcuts import render, redirect
from django.urls import reverse_lazy
#vistas
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

#models
from app.usuarios.usuario.models import Estudiante
from app.planificaciones.models import Planificacion
from app.bitacora.models import Bitacora

#forms
from app.bitacora.forms import BitacoraForm

# Create your views here.
class CrearBitacoraView(CreateView):
    model = Bitacora
    form_class = BitacoraForm
    template_name = 'bitacora/crearBitacora.html'  
    success_url = reverse_lazy('index')

class ListarBitacoraView(ListView):
    model = Bitacora
    template_name = 'bitacora/listarBitacora.html' 
    paginate_by = 10
    context_object_name = 'objects'  # Nombre de la variable en la plantilla que contiene la lista de Representantes
    
    def get_queryset(self):
        # Obtén la lista de representantes que deseas mostrar
        # Puedes filtrarlos de acuerdo a tus necesidades aquí
        return Bitacora.objects.all()
    
class VerBitacoraView(DetailView):
    model = Bitacora
    template_name = 'bitacora/verBitacora.html'  # Reemplaza 'usuarios/detalle_representante.html' con la ruta correcta a tu plantilla
    context_object_name = 'objects'  # Esto define el nombre de la variable en la plantilla


class EditarBitacoraView(UpdateView):
    model = Bitacora
    form_class = BitacoraForm
    template_name = 'bitacora/editarBitacora.html'
    success_url = reverse_lazy('listar_bitacora')

class EliminarBitacoraView(DeleteView):
    model = Bitacora
    template_name = 'bitacora/borrarBitacora.html' 
    success_url = reverse_lazy('listar_bitacora')

