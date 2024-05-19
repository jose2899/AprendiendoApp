from django.shortcuts import render, redirect, get_object_or_404
from .models import Paquete, Psicologo, DiaSemana, Asistencia, HorarioTerapia
from app.servicios.models import Paquete
from django.views.generic import View
from app.usuarios.usuario.models import Representante, Estudiante
from .forms import HorarioTerapiaForm, HorarioTerapiaFormSet, AsistenciaForm, FechaInicioForm
from django import forms
from django.contrib import messages
import calendar
from datetime import datetime, date
from django.forms import inlineformset_factory, modelformset_factory
import locale

class CrearHorarioView(View):
    template_name = 'terapia/crear_horario.html'
    
    def get(self, request, paquete_id):
        paquete = get_object_or_404(Paquete, pk=paquete_id)
        HorarioTerapiaFormSet = modelformset_factory(HorarioTerapia, form=HorarioTerapiaForm, extra=1)
        form_inicio = FechaInicioForm()
        formset = HorarioTerapiaFormSet(queryset=HorarioTerapia.objects.none(), form_kwargs={'paquete_id': paquete_id})
        return render(request, self.template_name, {'form_inicio': form_inicio, 'horario_formset': formset, 'paquete': paquete})

    def post(self, request, paquete_id):
        paquete = get_object_or_404(Paquete, pk=paquete_id)
        HorarioTerapiaFormSet = modelformset_factory(HorarioTerapia, form=HorarioTerapiaForm, extra=1)
        form_inicio = FechaInicioForm(request.POST)
        formset = HorarioTerapiaFormSet(request.POST, form_kwargs={'paquete_id': paquete_id})
        
        if form_inicio.is_valid() and formset.is_valid():
            fecha_inicio = form_inicio.cleaned_data['fecha_inicio']
            locale.setlocale(locale.LC_TIME, 'es_ES')
            dia_semana_inicio = fecha_inicio.strftime('%A').lower()

            dias_semana_ids = [form.cleaned_data['dia_semana'].id for form in formset if form.cleaned_data.get('dia_semana')]
            dias_semana_nombres = [DiaSemana.objects.get(pk=id).nombre.lower() for id in dias_semana_ids]
            if dia_semana_inicio not in dias_semana_nombres:
                messages.error(request, "La fecha de inicio debe coincidir con uno de los días seleccionados.")
                return render(request, self.template_name, {'form_inicio': form_inicio, 'horario_formset': formset, 'paquete': paquete})

            for form in formset:
                horario = form.save(commit=False)
                horario.paquete = paquete
                horario.fecha_inicio = fecha_inicio
                horario.save()
            return redirect('crear_horario', paquete_id=paquete.id)
        
        return render(request, self.template_name, {'form_inicio': form_inicio, 'horario_formset': formset, 'paquete': paquete})




#def detalle_paquete(request, estudiante_id):
   # Obtener todas las terapias asociadas al estudiante
#    terapias = Terapia.objects.filter(estudiante_id=estudiante_id)
    
    # Crear una lista para almacenar información de psicólogos, horarios y fecha de inicio
 #   info_psicologos_horas = []

    # Procesar el formulario para la fecha de inicio
#    if request.method == 'POST':
#        form = FechaTerapiaForm(request.POST)
#        if form.is_valid():
#            fecha_terapia = form.save(commit=False)
#            terapia_id = request.POST.get('terapia_id')  # Obtener el ID de la terapia
#            terapia = Terapia.objects.get(pk=terapia_id)
#            fecha_inicio = form.cleaned_data['fecha_inicio']
            # Verificar si la fecha de inicio corresponde a un día de la semana de los psicólogos de la terapia
            # Mapear el nombre del día de la semana de inglés a español
#            dias_semana_ingles = list(calendar.day_name)
#            dias_semana_espanol = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
#            dia_semana_fecha_inicio = dias_semana_espanol[dias_semana_ingles.index(fecha_inicio.strftime('%A'))]
#            horarios_psicologos = None
#            for terapia in terapias:
#                horarios_psicologos = Horario.objects.filter(terapia=terapia, dia_semana__nombre__iexact=f"{dia_semana_fecha_inicio}")
#                if horarios_psicologos.exists():
#                    break  # Salir del bucle si se encuentra una terapia con horarios en el día de la semana
#            if horarios_psicologos is not None and horarios_psicologos.exists():
                # Guardar la fecha de inicio solo si hay horarios de psicólogos para ese día de la semana
#                asignacion_fecha_terapia = AsignacionFechaTerapia(terapia=terapia, fecha_inicio=fecha_inicio)
#                asignacion_fecha_terapia.save()
#                return redirect('informacion_general', estudiante_id=estudiante_id)
#            else:
#                form.add_error('fecha_inicio', 'La fecha seleccionada no corresponde a un día de la semana con horarios de psicólogos.')
           #   # Redirigir a la misma página después de guardar la fecha
#    else:
#        form = FechaTerapiaForm()

#    for terapia in terapias:
#        horarios = Horario.objects.filter(terapia=terapia)
#        asignacion_fecha_terapia = None
#        asignacion_fecha_terapia = AsignacionFechaTerapia.objects.filter(terapia=terapia).first()
#        fecha_inicio = asignacion_fecha_terapia.fecha_inicio if asignacion_fecha_terapia else None
#        info_psicologos_horas.append({'terapia': terapia, 'horarios': horarios, 'fecha_inicio': fecha_inicio, 'form': form})

   # return render(request, 'terapia/detalle_paquete.html', {'info_psicologos_horas': info_psicologos_horas})




#def informacion_general(request, estudiante_id):
  #  estudiante = Estudiante.objects.get(pk=estudiante_id)
    # Obtener todas las terapias asociadas al estudiante
  #  terapias = Terapia.objects.filter(estudiante_id=estudiante_id)
     # Crear una lista para almacenar información de psicólogos y horarios
  #  info_psicologos_horas = []
    # Iterar sobre cada terapia y obtener la información del psicólogo y los horarios
  #  for terapia in terapias:
  #      horarios = Horario.objects.filter(terapia=terapia)
  #      info_psicologos_horas.append({'terapia': terapia, 'horarios': horarios, 'estudiante':estudiante})
  #  return render(request, 'terapia/informacion_general.html', {'info_psicologos_horas': info_psicologos_horas})

#horas_restantes = None  

#def registrar_asistencia(request):
 #   global horas_restantes
 #   if request.method == 'POST':
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            estudiante = form.cleaned_data['estudiante']
            asistio = form.cleaned_data['asistio']
            fecha = date.today()
            # Obtener el paquete asociado al estudiante seleccionado en el formulario
            paquete = Paquete.objects.filter(representante=estudiante.representante).first()
             # Inicializar horas_restantes solo si aún no ha sido asignado
            if horas_restantes is None:
                horas_restantes = paquete.horas

            # Restar una hora si el estudiante asistió
            if asistio:
                horas_restantes -= 1
            else:
                horas_restantes -= 1

            Asistencia.objects.create(estudiante=estudiante, fecha=fecha, asistio=asistio, horas_restantes=horas_restantes)
            return redirect('registrar_asistencia')
#    else:
        form = AsistenciaForm()
        estudiantes = Estudiante.objects.all()
        return render(request, 'terapia/registrar_asistencia.html', {'form': form, 'estudiantes': estudiantes})