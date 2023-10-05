

# Create your views here.
from django.shortcuts import render, redirect

# Create your views here.

from django.views import View
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from app.horario.models import Horario
from app.horario.forms import HorarioForm

class CrearHorarioView(CreateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'horarios/crearHorario.html'  
    success_url = reverse_lazy('index')

class ListarHorarioView(ListView):
    model = Horario
    template_name = 'horarios/listarHorario.html' 
    paginate_by = 10
    context_object_name = 'horarios'  # Nombre de la variable en la plantilla que contiene la lista de Representantes
    
    def get_queryset(self):
        # Obtén la lista de representantes que deseas mostrar
        # Puedes filtrarlos de acuerdo a tus necesidades aquí
        return Horario.objects.all()
    
class EliminarHorarioView(DeleteView):
    model = Horario
    template_name = 'horarios/eliminarHorario.html'  # Tu plantilla para confirmar la eliminación
    success_url = reverse_lazy('listar_horario')  # URL a la que redirigir después de eliminar

    
class EditarHorarioView(UpdateView):
    model = Horario
    form_class = HorarioForm
    template_name = 'horarios/editarHorario.html'
    success_url = reverse_lazy('listar_horario')

class VerHorarioView(DetailView):
    model = Horario
    template_name = 'horarios/verHorario.html'  # Reemplaza 'usuarios/detalle_representante.html' con la ruta correcta a tu plantilla
    context_object_name = 'objects'  # Esto define el nombre de la variable en la plantilla
