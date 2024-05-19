from django.shortcuts import render, redirect

#vistas
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

#imports Django
from django.urls import reverse_lazy

#models
from app.usuarios.psicologo.models import Psicologo

#forms
from app.usuarios.psicologo.forms import PsicologoForm

# Create your views here.

class CrearPsicologoView(CreateView):
    model = Psicologo
    form_class = PsicologoForm
    template_name = 'usuarios/crearPsicologo.html'  
    success_url = reverse_lazy('index')


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


class EliminarPsicologoView(DeleteView):
    model = Psicologo
    template_name = 'usuarios/eliminarPsicologo.html' 
    success_url = reverse_lazy('listar_psicologo')    