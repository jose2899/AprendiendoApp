from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from django.urls import reverse_lazy
#models
from app.planificaciones.models import Planificacion, PlanificacionSemana
from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico

#forms
from app.planificaciones.forms import PlanificacionForm, PlanificacionSemanaForm

# Create your views here.
class PlanificacionCreateView(CreateView):
    model = Planificacion
    form_class = PlanificacionForm
    template_name = 'planificaciones/planificacion.html' 
    
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Obtén el representante seleccionado del formulario
        estudiante_id = self.request.POST.get('estudiante')
        estudiante = Estudiante.objects.get(pk=estudiante_id)

        # Obtén el diagnostico seleccionado del formulario
        diagnostico_id = self.request.POST.get('diagnostico')
        diagnostico = Diagnostico.objects.get(pk=diagnostico_id)
        
        # Crea una instancia de Planificacion y asigna el estudiante y el diagnóstico seleccionados
        planificacion = form.save(commit=False)
        planificacion.estudiante = estudiante
        planificacion.diagnostico = diagnostico
        planificacion.save()

        return redirect('index')  

    

class PlanificacionListView(ListView):
    model = Planificacion
    template_name = 'planificaciones/listarPlanificacion.html'
    paginate_by = 10
    context_object_name = 'objects' 

class PlanificacionUpdateView(UpdateView):
    model = Planificacion
    form_class = PlanificacionForm
    template_name = 'planificaciones/editarPlanificacion.html'
    success_url = reverse_lazy('index')

class PlanificacionDeleteView(DeleteView):
    model = Planificacion
    template_name = 'planificaciones/borrarPlanificacion.html'
    success_url = reverse_lazy('lista_planificaciones')

class VerPlanificacionView(DetailView):
    model = Planificacion
    template_name = 'planificaciones/verPlanificacion.html' 
    context_object_name = 'objects' 

#semanas

class PlanificacionSemanaCreateView(CreateView):
    model = PlanificacionSemana
    form_class = PlanificacionSemanaForm
    template_name = 'planificaciones/planificacionSemana.html'
    context_object_name = 'semana'    

    def form_valid(self, form):
        # Obtén el representante seleccionado del formulario
        planificacion_id = self.request.POST.get('planificacion')
        planificacion = Planificacion.objects.get(pk=planificacion_id)
        
        # Crea una instancia de Estudiante y asigna el representante seleccionado
        planificacionSemana = form.save(commit=False)
        planificacionSemana.planificacion = planificacion
        planificacionSemana.save()
        return redirect('index')

    
# Vista para editar una semana existente
class PlanificacionSemanaUpdateView(UpdateView):
    model = PlanificacionSemana
    form_class = PlanificacionSemanaForm
    template_name = 'planificaciones/editarPSemana.html'
    context_object_name = 'semana'

    def get_queryset(self):
        planificacion = get_object_or_404(Planificacion, pk=self.kwargs['pk'])
        return PlanificacionSemana.objects.filter(planificacion=planificacion)
    
    def get_object(self, queryset=None):
        # Obtenemos el número de semana y el id de la planificación de la URL
        numero_semana = self.kwargs.get('pk1')
        planificacion_id = self.kwargs.get('pk')

        # Buscamos la planificación semanal correspondiente
        semana = get_object_or_404(PlanificacionSemana, planificacion__id=planificacion_id, numero_semana=numero_semana)
        return semana
    
# Vista para ver una semana específica
class PlanificacionSemanaDetailView(DetailView):
    model = PlanificacionSemana
    template_name = 'planificaciones/verPSemana.html'
    context_object_name = 'semana'
    def get_queryset(self):
        planificacion = get_object_or_404(Planificacion, pk=self.kwargs['pk'])
        return PlanificacionSemana.objects.filter(planificacion=planificacion)
    
    def get_object(self, queryset=None):
        # Obtenemos el número de semana y el id de la planificación de la URL
        numero_semana = self.kwargs.get('pk1')
        planificacion_id = self.kwargs.get('pk')

        # Buscamos la planificación semanal correspondiente
        semana = get_object_or_404(PlanificacionSemana, planificacion__id=planificacion_id, numero_semana=numero_semana)

        return semana
    

# Vista para listar todas las semanas de una planificación específica
class PlanificacionSemanaListView(ListView):
    model = PlanificacionSemana
    template_name = 'planificaciones/listarPSemana.html'
    context_object_name = 'semana'

    def get_queryset(self):
        planificacion = get_object_or_404(Planificacion, pk=self.kwargs['pk'])
        return PlanificacionSemana.objects.filter(planificacion=planificacion)

    def get_queryset(self):
        planificacion_id = self.kwargs['pk']
        semana_id = self.kwargs.get('pk1', None)
        # Obtener la planificación y, opcionalmente, la semana específica si se proporciona pk1
        if semana_id:
            return PlanificacionSemana.objects.filter(planificacion=planificacion_id, numero_semana=semana_id)
        else:
            return PlanificacionSemana.objects.filter(planificacion=planificacion_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['planificacion_id'] = self.kwargs['pk']  # Pasamos el ID de la planificación 
        planificacion = get_object_or_404(Planificacion, pk=self.kwargs['pk'])
        estudiante = planificacion.estudiante if planificacion.estudiante else "Planificación"
        # Agrega el nombre al contexto
        context['estudiante'] = estudiante
        return context
    
    
    

class PlanificacionSemanaDeleteView(DeleteView):
    model = PlanificacionSemana
    template_name = 'planificaciones/borrarPSemana.html'
    success_url = reverse_lazy('listar_p_semana')  # Otra vista a la que redirigir después de borrar
    context_object_name = 'semana'
    
    def get_queryset(self):
        planificacion = get_object_or_404(Planificacion, pk=self.kwargs['pk'])
        return PlanificacionSemana.objects.filter(planificacion=planificacion)
    
    def get_object(self, queryset=None):
        # Obtenemos el número de semana y el id de la planificación de la URL
        numero_semana = self.kwargs.get('pk1')
        planificacion_id = self.kwargs.get('pk')

        # Buscamos la planificación semanal correspondiente
        semana = get_object_or_404(PlanificacionSemana, planificacion__id=planificacion_id, numero_semana=numero_semana)

        return semana