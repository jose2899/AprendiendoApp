#vistas
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

#imports Django
from django.contrib.auth.models import User
from django.urls import reverse_lazy

#models
from app.usuarios.adminis.models import Adminis

#forms
from app.usuarios.adminis.forms import AdminisForm

class CrearAdminisView(CreateView):
    model = Adminis
    form_class = AdminisForm
    template_name = 'usuarios/crearAdmin.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Crear un usuario
        user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'], email=form.cleaned_data['email'])

        # Guardar el admin y relacionarlo con el usuario
        self.object = form.save(commit=False)
        self.object.user = user
        self.object.save()

        return super().form_valid(form)

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

class EditarAdminisView(UpdateView):
    model = Adminis
    form_class = AdminisForm
    template_name = 'usuarios/editarAdmin.html'
    success_url = reverse_lazy('listar_admin')

class EliminarAdminisView(DeleteView):
    model = Adminis
    template_name = 'usuarios/eliminarAdmin.html' 
    success_url = reverse_lazy('listar_admin')
