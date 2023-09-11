from django.shortcuts import render, redirect

#vistas
from django.views.generic import CreateView, ListView, DetailView
#imports Django
from django.urls import reverse_lazy
#models
from app.usuarios.usuario.models import Representante, Estudiante

#forms
from app.usuarios.usuario.forms import RepresentanteForm, EstudianteForm

# Create your views here.

class CrearRepresentanteView(CreateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'usuarios/crearUsuarios.html'  
    success_url = reverse_lazy('index')

class ListarRepresentanteView(ListView):
    model = Representante
    template_name = 'usuarios/listarUsuarios.html' 
    paginate_by = 10
    context_object_name = 'objects'  # Nombre de la variable en la plantilla que contiene la lista de Representantes

class CrearEstudianteView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'usuarios/crearEstudiantes.html' 
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Obtén el representante seleccionado del formulario
        representante_id = self.request.POST.get('representante')
        representante = Representante.objects.get(pk=representante_id)
        
        # Crea una instancia de Estudiante y asigna el representante seleccionado
        estudiante = form.save(commit=False)
        estudiante.representante = representante
        estudiante.save()

        return redirect('index')  # Redirige a donde desees después de crear al estudiante


class ListarEstudianteView(ListView):
    model = Estudiante
    template_name = 'usuarios/listarEstudiantes.html'
    paginate_by = 10
    context_object_name = 'objects' 


class VerRepresentanteView(DetailView):
    model = Representante
    template_name = 'usuarios/verRepresentante.html'  # Reemplaza 'usuarios/detalle_representante.html' con la ruta correcta a tu plantilla
    context_object_name = 'representante'  # Esto define el nombre de la variable en la plantilla
