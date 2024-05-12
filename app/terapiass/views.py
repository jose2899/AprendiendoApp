from django.shortcuts import render, redirect, get_object_or_404
from .models import Terapia, Horario, Paquete, Psicologo, Horario, DiaSemana, AsignacionFechaTerapia, Asistencia
from app.servicios.models import Paquete
from app.usuarios.usuario.models import Representante, Estudiante
from .forms import TerapiaForm, HorarioForm, HorarioFormSet, FechaTerapiaForm, AsistenciaForm
from django import forms
from django.contrib import messages
import calendar
from datetime import datetime, date

def crear_terapia(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'save':
            terapia_form = TerapiaForm(request.POST)
            horario_formset = HorarioFormSet(request.POST)
            
            if terapia_form.is_valid() and horario_formset.is_valid():
                terapia = terapia_form.save()

                for form in horario_formset:
                    if form.cleaned_data:
                        horario = form.save(commit=False)
                        horario.terapia = terapia
                        horario.save()

                # Guardar los estudiantes seleccionados en la terapia
                return redirect('agregar_estudiante', terapia_id=terapia.id)
        
        elif action == 'add_psicologo':
            terapia_form = TerapiaForm(request.POST)
            horario_formset = HorarioFormSet(request.POST)
            
            if terapia_form.is_valid() and horario_formset.is_valid():
                # Guardar la nueva terapia sin commit para crear una nueva instancia
                terapia_nueva = terapia_form.save(commit=False)
                terapia_nueva.pk = None
                terapia_nueva.id = None
                terapia_nueva.save()
                
                for form in horario_formset:
                    if form.cleaned_data:
                        horario_n = form.save(commit=False)
                        horario_n.terapia = terapia_nueva
                        horario_n.pk = None  # Crear una nueva instancia
                        horario_n.id = None
                        horario_n.save()
                
                # Redirigir a agregar psicólogo en la nueva terapia
                
                # Redirigir a agregar psicólogo en la nueva terapia
                return redirect('agregar_psicologo', terapia_id=terapia_nueva.id)
    else:
        terapia_form = TerapiaForm()
        horario_formset = HorarioFormSet()

        paquete_id = request.GET.get('paquete_id')
        if paquete_id:
            paquete = Paquete.objects.get(pk=paquete_id)
            
            representantes = Representante.objects.filter(paquete=paquete)
            estudiantes = Estudiante.objects.filter(representante__in=representantes)
            
            terapia_form.fields['estudiantes'].queryset = estudiantes
    return render(request, 'terapia/crear_terapia.html', {'terapia_form': terapia_form, 'horario_formset': horario_formset})


def agregar_psicologo(request, terapia_id):
    terapia = get_object_or_404(Terapia, id=terapia_id)

    if request.method == 'POST':
        form = TerapiaForm(request.POST, instance=terapia)
        horario_formset = HorarioFormSet(request.POST, instance=terapia)
        
        if form.is_valid() and horario_formset.is_valid():
            psicologo = form.cleaned_data['psicologo']
            estudiante = form.cleaned_data['estudiante']
            # Crear una nueva instancia de Terapia con el mismo paquete
            terapia_nueva = Terapia(paquete=terapia.paquete, psicologo=psicologo, estudiante=estudiante)
            terapia_nueva.save()

            for form in horario_formset:
                if form.cleaned_data:
                    horario = form.save(commit=False)
                    horario.terapia = terapia_nueva
                    horario.pk = None  # Crear una nueva instancia
                    horario.id = None
                    horario.save()
            return redirect('agregar_psicologo', terapia_id=terapia_nueva.id)
    else:
        form = TerapiaForm(instance=terapia)
        form.fields['paquete'].widget = forms.HiddenInput()
        horario_formset = HorarioFormSet(instance=terapia)

         # Obtener el paquete asociado a la terapia
        paquete = terapia.paquete
        
        # Obtener todos los representantes asociados al paquete
        representantes = Representante.objects.filter(paquete=paquete)
        
        # Obtener todos los estudiantes que son hijos de esos representantes
        estudiantes = Estudiante.objects.filter(representante__in=representantes)
        
        # Pasar esos estudiantes al formulario de creación de terapia


    return render(request, 'terapia/agregar_psicologo.html', {'form': form, 'terapia': terapia, 'horario_formset': horario_formset})


def detalle_paquete(request, estudiante_id):
   # Obtener todas las terapias asociadas al estudiante
    terapias = Terapia.objects.filter(estudiante_id=estudiante_id)
    
    # Crear una lista para almacenar información de psicólogos, horarios y fecha de inicio
    info_psicologos_horas = []

    # Procesar el formulario para la fecha de inicio
    if request.method == 'POST':
        form = FechaTerapiaForm(request.POST)
        if form.is_valid():
            fecha_terapia = form.save(commit=False)
            terapia_id = request.POST.get('terapia_id')  # Obtener el ID de la terapia
            terapia = Terapia.objects.get(pk=terapia_id)
            fecha_inicio = form.cleaned_data['fecha_inicio']
            # Verificar si la fecha de inicio corresponde a un día de la semana de los psicólogos de la terapia
            # Mapear el nombre del día de la semana de inglés a español
            dias_semana_ingles = list(calendar.day_name)
            dias_semana_espanol = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
            dia_semana_fecha_inicio = dias_semana_espanol[dias_semana_ingles.index(fecha_inicio.strftime('%A'))]
            horarios_psicologos = None
            for terapia in terapias:
                horarios_psicologos = Horario.objects.filter(terapia=terapia, dia_semana__nombre__iexact=f"{dia_semana_fecha_inicio}")
                if horarios_psicologos.exists():
                    break  # Salir del bucle si se encuentra una terapia con horarios en el día de la semana
            if horarios_psicologos is not None and horarios_psicologos.exists():
                # Guardar la fecha de inicio solo si hay horarios de psicólogos para ese día de la semana
                asignacion_fecha_terapia = AsignacionFechaTerapia(terapia=terapia, fecha_inicio=fecha_inicio)
                asignacion_fecha_terapia.save()
                return redirect('informacion_general', estudiante_id=estudiante_id)
            else:
                form.add_error('fecha_inicio', 'La fecha seleccionada no corresponde a un día de la semana con horarios de psicólogos.')
           #   # Redirigir a la misma página después de guardar la fecha
    else:
        form = FechaTerapiaForm()

    for terapia in terapias:
        horarios = Horario.objects.filter(terapia=terapia)
        asignacion_fecha_terapia = None
        asignacion_fecha_terapia = AsignacionFechaTerapia.objects.filter(terapia=terapia).first()
        fecha_inicio = asignacion_fecha_terapia.fecha_inicio if asignacion_fecha_terapia else None
        info_psicologos_horas.append({'terapia': terapia, 'horarios': horarios, 'fecha_inicio': fecha_inicio, 'form': form})

    return render(request, 'terapia/detalle_paquete.html', {'info_psicologos_horas': info_psicologos_horas})


def informacion_general(request, estudiante_id):
    estudiante = Estudiante.objects.get(pk=estudiante_id)
    # Obtener todas las terapias asociadas al estudiante
    terapias = Terapia.objects.filter(estudiante_id=estudiante_id)
     # Crear una lista para almacenar información de psicólogos y horarios
    info_psicologos_horas = []
    # Iterar sobre cada terapia y obtener la información del psicólogo y los horarios
    for terapia in terapias:
        horarios = Horario.objects.filter(terapia=terapia)
        info_psicologos_horas.append({'terapia': terapia, 'horarios': horarios, 'estudiante':estudiante})
    return render(request, 'terapia/informacion_general.html', {'info_psicologos_horas': info_psicologos_horas})

horas_restantes = None  

def registrar_asistencia(request):
    global horas_restantes
    if request.method == 'POST':
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
    else:
        form = AsistenciaForm()
        estudiantes = Estudiante.objects.all()
        return render(request, 'terapia/registrar_asistencia.html', {'form': form, 'estudiantes': estudiantes})