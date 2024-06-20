
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from app.terapiass.models import HorarioTerapia
from app.horarios.models import Asistencia
from django.views import View
from app.horarios.forms import AsistenciaForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from app.controlRoles.utils import permission_required_custom

@permission_required_custom('psicologo.can_create_psicologo')
@login_required
def listar_horarios(request):
    psicologo = request.user.psicologo  
    hoy = timezone.now().date()
    horarios = HorarioTerapia.objects.filter(psicologo=psicologo, fecha_dia=hoy)
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

def es_psicologo(user):
    return hasattr(user, 'psicologo')

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(es_psicologo), name='dispatch')
class RegistrarAsistenciaView(View):
    template_name = 'horarios/registrarAsistencia.html'
    def get(self, request, horario_id):
        horario = get_object_or_404(HorarioTerapia, pk=horario_id)
        estudiante = horario.paquete.estudiante
        fecha_actual = timezone.now().date()
        context = {
            'horario': horario,
            'estudiante': estudiante,
            'fecha_actual': fecha_actual,
        }
        return render(request, self.template_name, context)

    def post(self, request, horario_id):
        horario = get_object_or_404(HorarioTerapia, pk=horario_id)
        asistencia, created = Asistencia.objects.get_or_create(
            horario=horario,
            fecha=timezone.now().date()
        )
        asistencia.asistencia = 'asistio' in request.POST
        asistencia.save()
        messages.success(request, 'Asistencia registrada correctamente.')
        return render(request, self.template_name, {'horario': horario, 'estudiante': horario.paquete.estudiante, 'fecha_actual': timezone.now().date()})