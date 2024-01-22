
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from app.terapiass.forms import TerapiaForm, AsignacionEstudianteForm, AsignacionPsicologoForm, HorarioTerapiaForm, HorarioTerapiaFormSet, formset_factory
from app.usuarios.usuario.models import Estudiante, Representante
from app.terapiass.models import Terapia, AsignacionEstudiante, AsignacionPsicologo, HorarioTerapia
from app.usuarios.psicologo.models import Psicologo
from app.terapiass.models import Terapia, DiaSemana
from django.contrib import messages
from django.views.generic import DetailView

from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime, timedelta
from app.terapiass.utils import calculate_start_date
from django.forms import formset_factory

from django.urls import reverse

# Create your views here.
# terapias/views.py


class CrearTerapiaView(View):
    def get(self, request):
        terapia_form = TerapiaForm()
        asignacion_form = AsignacionPsicologoForm()
        horario_form = HorarioTerapiaForm()

        return render(request, 'terapia/crear_terapia.html', {
            'terapia_form': terapia_form,
            'asignacion_form': asignacion_form,
            'horario_form': horario_form,
        })
    def post(self, request):
        terapia_form = TerapiaForm(request.POST)
        asignacion_form = AsignacionPsicologoForm(request.POST)
        psicologo_forms = request.POST.getlist('psicologo')
        dias_semana_forms = request.POST.getlist('dia_semana')
        horario_form = HorarioTerapiaForm(request.POST)

        if terapia_form.is_valid() and asignacion_form.is_valid() and horario_form.is_valid():
            terapia = terapia_form.save()

            # Obtén la fecha de inicio del formulario
            start_date = terapia_form.cleaned_data['fecha_inicio']

            # Define un diccionario para mapear números de días de semana a nombres
            dias_semana_dict = {
                '1': 'Lunes',
                '2': 'Martes',
                '3': 'Miércoles',
                '4': 'Jueves',
                '5': 'Viernes',
                '6': 'Sábado',
                '7': 'Domingo',
            }

            # Traduce los números de los días de la semana a nombres
            dias_semana_nombres = [dias_semana_dict[dia] for dia in dias_semana_forms]

            # Verifica que la fecha de inicio coincida con al menos uno de los días de la semana seleccionados
            valid_start_date = False
            start_weekday = start_date.isoweekday()  # Obtiene el número del día de la semana de la fecha de inicio

            for dia_semana in dias_semana_forms:
                if start_weekday == int(dia_semana):
                    valid_start_date = True
                    break

            if not valid_start_date:
                messages.error(request, "La fecha de inicio debe coincidir con al menos uno de los días de la semana seleccionados.")
                return redirect('crear_terapia')
             # Obtén los psicólogos seleccionados en el formulario de asignación


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


class AgregarHorarioTerapiaView(View):
    def get(self, request, terapia_id):
        terapia = Terapia.objects.get(pk=terapia_id)
        asignaciones = AsignacionPsicologo.objects.filter(terapia=terapia)
        formset = HorarioTerapiaFormSet(queryset=HorarioTerapia.objects.none(), form_kwargs={'terapia': terapia})
        context = {
            'terapia': terapia,
            'asignaciones': asignaciones,
            'formset': formset,
        }
        return render(request, 'terapia/agregar_horario_terapia.html', context)

    def post(self, request, terapia_id):
        terapia = Terapia.objects.get(pk=terapia_id)
        asignaciones = AsignacionPsicologo.objects.filter(terapia=terapia)
        formset = HorarioTerapiaFormSet(request.POST, queryset=HorarioTerapia.objects.none(), form_kwargs={'terapia': terapia})
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            return redirect('terapia_detail', terapia_id=terapia.id)
        context = {
            'terapia': terapia,
            'asignaciones': asignaciones,
            'formset': formset,
        }
        return render(request, 'terapia/agregar_horario_terapia.html', context)