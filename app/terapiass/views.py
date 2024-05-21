from django.shortcuts import render, redirect, get_object_or_404
from .models import Paquete, Psicologo, DiaSemana, Asistencia, HorarioTerapia
from app.servicios.models import Paquete
from django.views.generic import View
from app.usuarios.usuario.models import Representante, Estudiante
from .forms import HorarioTerapiaForm, HorarioTerapiaFormSet, AsistenciaForm, FechaInicioForm
from django import forms
from django.contrib import messages
import calendar
from datetime import datetime, date, timedelta
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
            fecha_inicio_original = form_inicio.cleaned_data['fecha_inicio']
            fecha_inicio = fecha_inicio_original
            locale.setlocale(locale.LC_TIME, 'es_ES')

            dias_semana_ids = [form.cleaned_data['dia_semana'].id for form in formset if form.cleaned_data.get('dia_semana')]
            if not dias_semana_ids:
                messages.error(request, "Debe seleccionar al menos un día de la semana.")
                return render(request, self.template_name, {'form_inicio': form_inicio, 'horario_formset': formset, 'paquete': paquete})
            
            dia_semana_inicio = fecha_inicio.strftime('%A').lower()
            print("dia de incio", dia_semana_inicio)
            dias_semana_nombres = [DiaSemana.objects.get(pk=id).nombre.lower() for id in dias_semana_ids]
            print("dias semana", dias_semana_nombres)
            if dia_semana_inicio not in dias_semana_nombres:
                messages.error(request, "La fecha de inicio debe coincidir con uno de los días seleccionados.")
                return render(request, self.template_name, {'form_inicio': form_inicio, 'horario_formset': formset, 'paquete': paquete})

            total_horas = paquete.horas
            horas_programadas = 0
            horarios_creados = []

            while horas_programadas < total_horas:
                for form in formset:
                    if horas_programadas >= total_horas:
                        break
                    
                    horario = form.save(commit=False)
                    horario.paquete = paquete
                    horario.fecha_inicio = fecha_inicio_original
                    horario.fecha_dia = obtener_fecha_para_dia(fecha_inicio, form.cleaned_data['dia_semana'].id)
                    horario.save()
                    horarios_creados.append(horario)
                    horas_programadas += 1
                
                # Incrementar la semana
                fecha_inicio += timedelta(weeks=1)
                # Crear horarios adicionales para completar las horas del paquete
                for dia_semana_id in dias_semana_ids:
                    if horas_programadas >= total_horas:
                        break
                    nuevo_horario = HorarioTerapia(
                        paquete=paquete,
                        psicologo=form.cleaned_data['psicologo'],
                        dia_semana=DiaSemana.objects.get(pk=dia_semana_id),
                        hora_inicio=form.cleaned_data['hora_inicio'],
                        fecha_inicio = fecha_inicio_original,
                        fecha_dia=obtener_fecha_para_dia(fecha_inicio, dia_semana_id)
                    )
                    nuevo_horario.save()
                    horarios_creados.append(nuevo_horario)
                    horas_programadas += 1
                
            messages.success(request, f"{len(horarios_creados)} horarios creados con éxito.")
            return redirect('crear_horario', paquete_id=paquete.id)
        return render(request, self.template_name, {'form_inicio': form_inicio, 'horario_formset': formset, 'paquete': paquete})

def obtener_fecha_para_dia(fecha_inicio, dia_semana_id):
    # Obtener el día de la semana como número (0=lunes, 6=domingo)
    dia_semana_nombre = DiaSemana.objects.get(pk=dia_semana_id).nombre.lower()
    dias_semana_dict = {
        'lunes': 0,
        'martes': 1,
        'miércoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'domingo': 6
    }
    dia_semana_numero = dias_semana_dict[dia_semana_nombre]

    # Obtener el día de la semana de la fecha de inicio
    dia_inicio_numero = fecha_inicio.weekday()  # 0=lunes, 6=domingo

    # Calcular la diferencia en días
    diferencia_dias = (dia_semana_numero - dia_inicio_numero) % 7

    # Obtener la fecha del día seleccionado
    fecha_dia_seleccionado = fecha_inicio + timedelta(days=diferencia_dias)
    print("uso de la funcion del dia", fecha_dia_seleccionado)
    return fecha_dia_seleccionado
    


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
 #       form = AsistenciaForm(request.POST)
 #       if form.is_valid():
 #           estudiante = form.cleaned_data['estudiante']
 #           asistio = form.cleaned_data['asistio']
 #           fecha = date.today()
            # Obtener el paquete asociado al estudiante seleccionado en el formulario
 #           paquete = Paquete.objects.filter(representante=estudiante.representante).first()
             # Inicializar horas_restantes solo si aún no ha sido asignado
 #           if horas_restantes is None:
 #               horas_restantes = paquete.horas

            # Restar una hora si el estudiante asistió
 #           if asistio:
 #               horas_restantes -= 1
 #           else:
 #               horas_restantes -= 1

   #         Asistencia.objects.create(estudiante=estudiante, fecha=fecha, asistio=asistio, horas_restantes=horas_restantes)
   #         return redirect('registrar_asistencia')
#    else:
    #    form = AsistenciaForm()
     #   estudiantes = Estudiante.objects.all()
      #  return render(request, 'terapia/registrar_asistencia.html', {'form': form, 'estudiantes': estudiantes})