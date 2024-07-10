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
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#forms
from app.bitacora.forms import BitacoraForm, NuevaBitacoraForm

# Create your views here.
class CrearBitacoraView(CreateView):
    model = Bitacora
    form_class = BitacoraForm
    template_name = 'bitacora/crearBitacora.html'  
    success_url = reverse_lazy('crear_bitacora')
    def form_valid(self, form):
        try:
            bitacora = form.save()
            messages.success(self.request, 'Bitacora creada correctamente.')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'No se ha creado correctamente la bitacora: {e}')
            return redirect('crear_bitacora')

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
        return Bitacora.objects.all()  
    
class VerBitacoraView(DetailView):
    model = Bitacora
    template_name = 'bitacora/verBitacora.html'
    context_object_name = 'bitacora'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bitacora_id = self.kwargs.get('pk')
        bitacora = get_object_or_404(Bitacora, pk=bitacora_id)

        nuevas_bitacoras_list = NuevaBitacora.objects.filter(bitacora=bitacora)

        # Paginación
        paginator = Paginator(nuevas_bitacoras_list, 10)  # Mostrar 10 bitácoras por página
        page = self.request.GET.get('page')

        try:
            nuevas_bitacoras = paginator.page(page)
        except PageNotAnInteger:
            nuevas_bitacoras = paginator.page(1)
        except EmptyPage:
            nuevas_bitacoras = paginator.page(paginator.num_pages)

        context['nuevas_bitacoras'] = nuevas_bitacoras
        context['is_paginated'] = nuevas_bitacoras.has_other_pages()
        context['page_obj'] = nuevas_bitacoras
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
    model = NuevaBitacora
    template_name = 'bitacora/crear_nueva_bitacora.html'
    form_class = NuevaBitacoraForm
    context_object_name = 'Nuevabitacora'

    def form_valid(self, form):
        try:
            bitacora_id = self.kwargs.get('bitacora_id')
            bitacora = get_object_or_404(Bitacora, pk=bitacora_id)
            form.instance.bitacora = bitacora
            messages.success(self.request, 'Bitacora diaria creada correctamente.')
            return super().form_valid(form)
        except Exception as e:
            # Si ocurre un error, añade un mensaje de error
            messages.error(self.request, f'No se ha creado correctamente la bitacora diaria {e}')
            return reverse('crear_nueva_bitacora')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bitacora_id = self.kwargs.get('bitacora_id')
        bitacora = get_object_or_404(Bitacora, pk=bitacora_id)
        context['bitacora'] = bitacora
        return context

    def get_success_url(self):
        return reverse('ver_bitacora', kwargs={'pk': self.object.bitacora.id})
    
class EditarNuevaBitacoraView(UpdateView):
    model = NuevaBitacora
    form_class = NuevaBitacoraForm
    template_name = 'bitacora/editar_nueva_bitacora.html'
    context_object_name = 'Nuevabitacora'

    def get_object(self, queryset=None):
        nueva_id = self.kwargs.get('nueva_id')
        return get_object_or_404(NuevaBitacora, id=nueva_id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bitacora'] = self.object.bitacora  # Accede a la bitacora directamente desde el objeto
        return context

    def get_success_url(self):
        return reverse('ver_bitacora', kwargs={'pk': self.object.bitacora.id})
    
class EliminarNuevaBitacoraView(DeleteView):
    model = NuevaBitacora
    template_name = 'bitacora/eliminar_nueva_bitacora.html'
    context_object_name = 'Nuevabitacora'
    
    def get_object(self, queryset=None):
        nueva_id = self.kwargs.get('nueva_id')
        return get_object_or_404(NuevaBitacora, id=nueva_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bitacora'] = self.object.bitacora  # Accede a la bitacora directamente desde el objeto
        return context

    def get_success_url(self):
        return reverse_lazy('ver_bitacora', kwargs={'pk': self.object.bitacora.id})