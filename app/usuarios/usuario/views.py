from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from app.controlRoles.utils import permission_required_custom
from datetime import date
#vistas
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
#imports Django
from django.urls import reverse_lazy
#models
from app.usuarios.usuario.models import Representante, Estudiante

#forms
from app.usuarios.usuario.forms import RepresentanteForm, EstudianteForm

# Create your views here.
@method_decorator(permission_required('adminis.can_create_adminis'), name='dispatch')
class CrearRepresentanteView(CreateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'usuarios/crearUsuarios.html'  
    success_url = reverse_lazy('index')

class ListarRepresentanteView(ListView):
    model = Representante
    template_name = 'usuarios/listarUsuarios.html' 
    paginate_by = 10
    context_object_name = 'objects'  
    
    def get_queryset(self):
        return Representante.objects.all()
    
@method_decorator(permission_required('adminis.can_create_adminis'), name='dispatch')
class CrearEstudianteView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'usuarios/crearEstudiantes.html' 
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Obtén el representante seleccionado del formulario
        representante_id = self.request.POST.get('representante')
        representante = Representante.objects.get(pk=representante_id)
        # Calcular la edad basada en la fecha de nacimiento
        fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
        today = date.today()
        edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        # Asignar la edad al formulario antes de guardarlo
        form.instance.edad = edad
        # Crea una instancia de Estudiante y asigna el representante seleccionado
        estudiante = form.save(commit=False)
        estudiante.representante = representante
        estudiante.save()

        return redirect('index') 


class ListarEstudianteView(ListView):
    model = Estudiante
    template_name = 'usuarios/listarEstudiantes.html'
    paginate_by = 10
    context_object_name = 'objects' 


class VerRepresentanteView(DetailView):
    model = Representante
    template_name = 'usuarios/verRepresentante.html' 
    context_object_name = 'representante'  

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EditarRepresentanteView(UpdateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'usuarios/editarRepresentante.html'
    success_url = reverse_lazy('listar_representantes')

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EliminarRepresentanteView(DeleteView):
    model = Representante
    template_name = 'usuarios/eliminarRepresentante.html' 
    success_url = reverse_lazy('listar_representantes')


class VerEstudianteView(DetailView):
    model = Estudiante
    template_name = 'usuarios/verEstudiante.html' 
    context_object_name = 'objects'  

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EditarEstudianteView(UpdateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = 'usuarios/editarEstudiante.html'
    success_url = reverse_lazy('listar_estudiantes')
    def form_valid(self, form):
        # Calcular la edad basada en la fecha de nacimiento actualizada
        fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
        today = date.today()
        edad = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        # Asignar la edad actualizada al objeto Estudiante antes de guardarlo
        form.instance.edad = edad
        
        # Llamar al método form_valid() de la clase base para guardar el formulario
        return super().form_valid(form)

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EliminarEstudianteView(DeleteView):
    model = Estudiante
    template_name = 'usuarios/eliminarEstudiante.html' 
    success_url = reverse_lazy('listar_estudiantes')

    