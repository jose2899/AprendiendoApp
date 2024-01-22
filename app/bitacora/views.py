from django.shortcuts import render, redirect
from django.urls import reverse_lazy
#vistas
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

#models
from app.usuarios.usuario.models import Estudiante
from app.planificaciones.models import Planificacion
from app.bitacora.models import Bitacora
from app.terapiass.models import Diagnostico

#forms
from app.bitacora.forms import BitacoraForm, NuevaBitacoraForm

# Create your views here.
class CrearBitacoraView(CreateView):
    model = Bitacora
    form_class = BitacoraForm
    template_name = 'bitacora/crearBitacora.html'  
    success_url = reverse_lazy('index')

class ListarBitacoraView(ListView):
    model = Bitacora
    template_name = 'bitacora/listarBitacora.html'
    context_object_name = 'bitacoras'
    paginate_by = 10 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén la lista de todos los estudiantes que tienen bitácoras
        context['estudiantes_con_bitacoras'] = Bitacora.objects.values_list('estudiante__nombre', flat=True).distinct()
        return context

    def get_queryset(self):
        return Bitacora.objects.all()  # Puedes ajustar esto según tus necesidades
    
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

class CrearNuevaBitacoraView(CreateView):
    model = Bitacora
    form_class = NuevaBitacoraForm
    template_name = 'bitacora/crearNuevaBitacora.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Asigna el estudiante actual antes de guardar la nueva bitácora
        estudiante_id = self.kwargs['estudiante_id']
        estudiante = Estudiante.objects.get(id=estudiante_id)
        form.instance.estudiante = estudiante
        form.instance.planificacion = estudiante.bitacora.planificacion  # Ajusta según tus necesidades
        form.instance.diagnostico = estudiante.bitacora.diagnostico  # Ajusta según tus necesidades
        return super().form_valid(form)
    
class DetalleBitacoraView(DetailView):
    model = Bitacora
    template_name = 'bitacora/detalleBitacora.html'
    context_object_name = 'bitacora'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener bitácoras anteriores del estudiante
        context['bitacoras_estudiante'] = Bitacora.objects.filter(estudiante=context['bitacora'].estudiante).exclude(pk=context['bitacora'].pk)
        context['nueva_bitacora_form'] = BitacoraForm()
        return context