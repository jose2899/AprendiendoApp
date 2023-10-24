
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from app.terapiass.forms import TerapiaForm, AsignacionEstudianteForm, AsignacionPsicologoForm, AsignacionPsicologoFormSet
from app.usuarios.usuario.models import Estudiante, Representante
from app.terapiass.models import Terapia, AsignacionEstudiante, AsignacionPsicologo
from app.usuarios.psicologo.models import Psicologo
from app.terapiass.models import Terapia
from datetime import datetime, timedelta
from app.terapiass.utils import calculate_start_date
from django.urls import reverse

# Create your views here.
# terapias/views.py


class CrearTerapiaView(View):
    def get(self, request):
        terapia_form = TerapiaForm()
        asignacion_form = AsignacionPsicologoForm()
        return render(request, 'terapia/crear_terapia.html', {'terapia_form': terapia_form, 'asignacion_form': asignacion_form})

    def post(self, request):
        terapia_form = TerapiaForm(request.POST)
        asignacion_form = AsignacionPsicologoForm(request.POST)
        psicologo_forms = request.POST.getlist('psicologo')
        dias_semana_forms = request.POST.getlist('dia_semana')

        if terapia_form.is_valid() and asignacion_form.is_valid():
            terapia = terapia_form.save()

            for i, psicologo_id in enumerate(psicologo_forms):
                # Crea una instancia de AsignacionPsicologo para cada psicólogo seleccionado
                asignacion = AsignacionPsicologo(terapia=terapia, psicologo_id=psicologo_id)
                asignacion.save()
                
                # Asigna los días de la semana seleccionados de forma independiente para cada psicólogo
                dias_semana = dias_semana_forms[i]
                asignacion.dia_semana.set(dias_semana)

            return redirect('asignar_estudiante')

        return render(request, 'terapia/crear_terapia.html', {'terapia_form': terapia_form, 'asignacion_form': asignacion_form})

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

