
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from app.terapiass.models import HorarioTerapia
from app.horarios.models import Asistencia
from django.views import View
from app.horarios.forms import AsistenciaForm

@login_required
def listar_horarios(request):
    psicologo = request.user.psicologo  
    hoy = timezone.now().date()
    horarios = HorarioTerapia.objects.filter(psicologo=psicologo, fecha_dia=hoy)
    print(f"Total horarios encontrados: {horarios.count()}")  
    # Asegurarse de que se obtienen los datos del estudiante y representante
    horarios_info = []
    for horario in horarios:
            paquete = horario.paquete
            estudiante = paquete.estudiante
            representante = estudiante.representante
            horarios_info.append({
                'horario': horario,
                'estudiante': estudiante,
                'representante': representante,
                'hora_inicio': horario.hora_inicio,
                'dia_semana': horario.dia_semana.nombre,
                'fecha_inicio': horario.fecha_inicio,
            })
    return render(request, 'horarios/listarHorarios.html', {'horarios_info': horarios_info})


@login_required
def listar_todos_horarios(request):
    psicologo = request.user.psicologo  
    horarios = HorarioTerapia.objects.filter(psicologo=psicologo).order_by('fecha_dia')

    # Asegurarse de que se obtienen los datos del estudiante y representante
    horarios_info = []
    for horario in horarios:
            paquete = horario.paquete
            estudiante = paquete.estudiante
            representante = estudiante.representante
            horarios_info.append({
                'horario': horario,
                'estudiante': estudiante,
                'representante': representante,
                'hora_inicio': horario.hora_inicio,
                'dia_semana': horario.dia_semana.nombre,
                'fecha_inicio': horario.fecha_inicio,
            })
    return render(request, 'horarios/listarTodosHorarios.html', {'horarios_info': horarios_info})



class RegistrarAsistenciaView(View):
    def get(self, request, horario_id):
        horario = get_object_or_404(HorarioTerapia, pk=horario_id)
        form = AsistenciaForm()
        return render(request, 'horarios/registrarAsistencia.html', {'form': form, 'horario': horario})

    def post(self, request, horario_id):
        horario = get_object_or_404(HorarioTerapia, pk=horario_id)
        form = AsistenciaForm(request.POST)
        if form.is_valid():
            asistencia = form.save(commit=False)
            asistencia.horario = horario
            asistencia.save()
            return redirect('listarHorarios')
        return render(request, 'horarios/registrarAsistencia.html', {'form': form, 'horario': horario})