from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from app.controlRoles.utils import permission_required_custom
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.shortcuts import redirect

#vistas
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

#imports Django
from django.contrib.auth.models import User
from django.urls import reverse_lazy

#models
from app.usuarios.adminis.models import Adminis

#forms
from app.usuarios.adminis.forms import AdminisForm

#actualizar permisos
@method_decorator(permission_required('adminis.can_create_adminis'), name='dispatch')
class CrearAdminisView(CreateView):
    model = Adminis
    form_class = AdminisForm
    template_name = 'usuarios/crearAdmin.html'
    success_url = reverse_lazy('crear_admin')

    def form_valid(self, form):
        # Crear un usuario
        user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])

        # Asignar el usuario al grupo Administradores
        admin_group = Group.objects.get(name='Administradores')
        user.groups.add(admin_group)
            
        # Guardar el admin y relacionarlo con el usuario
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()
        messages.success(self.request, 'Administrador creado correctamente.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Mensaje genérico cuando el formulario es inválido
        messages.error(self.request, f'No se pudo crear al Administrador.')
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuario_forms'] = AdminisForm()
        return context

class ListarAdminisView(ListView):
    model = Adminis
    template_name = 'usuarios/listarAdmin.html'
    paginate_by = 10
    context_object_name = 'objects'

class VerAdminisView(DetailView):
    model = Adminis
    template_name = 'usuarios/verAdmin.html'  
    context_object_name = 'objects'  

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EditarAdminisView(UpdateView):
    model = Adminis
    form_class = AdminisForm
    template_name = 'usuarios/editarAdmin.html'
    success_url = reverse_lazy('listar_admin')

@method_decorator(permission_required_custom('adminis.can_create_adminis'), name='dispatch')
class EliminarAdminisView(DeleteView):
    model = Adminis
    template_name = 'usuarios/eliminarAdmin.html' 
    success_url = reverse_lazy('listar_admin')
