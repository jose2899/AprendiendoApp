from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from app.controlRoles.utils import permission_required_custom
#vistas
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

#imports Django
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group

#models
from app.usuarios.psicologo.models import Psicologo

#forms
from app.usuarios.psicologo.forms import PsicologoForm

# Create your views here.
@method_decorator(permission_required('adminis.can_create_adminis'), name='dispatch')
class CrearPsicologoView(CreateView):
    model = Psicologo
    form_class = PsicologoForm
    template_name = 'usuarios/crearPsicologo.html'  
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Crear un usuario
        user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])

        # Asignar el usuario al grupo Psicólogos
        psicologo_group = Group.objects.get(name='Psicologos')
        user.groups.add(psicologo_group)

        # Guardar el psicólogo y relacionarlo con el usuario
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_forms'] = PsicologoForm()
        return context

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EditarPsicologoView(UpdateView):
    model = Psicologo
    form_class = PsicologoForm
    template_name = 'usuarios/editarPsicologo.html'
    success_url = reverse_lazy('listar_psicologo')


class ListarPsicologoView(ListView):
    model = Psicologo
    template_name = 'usuarios/listarPsicologo.html'
    paginate_by = 10
    context_object_name = 'objects' 


class VerPsicologoView(DetailView):
    model = Psicologo
    template_name = 'usuarios/verPsicologo.html'  
    context_object_name = 'objects'  

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EliminarPsicologoView(DeleteView):
    model = Psicologo
    template_name = 'usuarios/eliminarPsicologo.html' 
    success_url = reverse_lazy('listar_psicologo')    