from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
#vistas
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

#models
from app.usuarios.usuario.models import Estudiante
from app.planificaciones.models import Planificacion
from app.bitacora.models import Bitacora, NuevaBitacora
from app.terapiass.models import Diagnostico
from django.urls import reverse

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
    template_name = 'bitacora/verBitacora.html'
    context_object_name = 'bitacora'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bitacora_id = self.kwargs.get('pk')
        bitacora = get_object_or_404(Bitacora, pk=bitacora_id)
        nuevas_bitacoras = NuevaBitacora.objects.filter(bitacora=bitacora)
        context['nuevas_bitacoras'] = nuevas_bitacoras
        return context


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
    template_name = 'bitacora/crear_nueva_bitacora.html'
    form_class = NuevaBitacoraForm

    def form_valid(self, form):
        bitacora_id = self.kwargs.get('bitacora_id')
        bitacora = get_object_or_404(Bitacora, pk=bitacora_id)
        form.instance.bitacora = bitacora
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('ver_bitacora', kwargs={'pk': self.object.bitacora.id})


    
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