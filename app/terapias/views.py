
from django.shortcuts import render, redirect
from django.views import View
from app.terapias.forms import TerapiaForm, AsignacionEstudianteForm
from app.usuarios.usuario.models import Estudiante, Representante
from app.terapias.models import Terapia, AsignacionEstudiante
# Create your views here.
# terapias/views.py


class CrearTerapiaView(View):
    def get(self, request):
        form = TerapiaForm()
        return render(request, 'terapia/crear_terapia.html', {'form': form})

    def post(self, request):
        form = TerapiaForm(request.POST)
        if form.is_valid():
            terapia = form.save()
            return redirect('asignar_estudiante', terapia_id=terapia.pk)
        return render(request, 'terapia/crear_terapia.html', {'form': form})

class AsignarEstudianteView(View):
    def get(self, request, terapia_id):
        terapia = Terapia.objects.get(pk=terapia_id)
        form = AsignacionEstudianteForm()
        return render(request, 'terapia/asignar_estudiante.html', {'form': form, 'terapia': terapia})

    def post(self, request, terapia_id):
        terapia = Terapia.objects.get(pk=terapia_id)
        form = AsignacionEstudianteForm(request.POST)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.terapia = terapia
            asignacion.save()
            return redirect('asignar_estudiante', terapia_id=terapia_id)
        return render(request, 'terapia/asignar_estudiante.html', {'form': form, 'terapia': terapia})
