from django.shortcuts import render, get_object_or_404

from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico
from app.planificaciones.models import Planificacion
from app.bitacora.models import NuevaBitacora

def listar_estudiantes_tdah(request):
    estudiantes_tdah = Planificacion.objects.filter(diagnostico__nombre_diagnostico='TDAH', estudiante__edad__range=(7, 8)).select_related('estudiante', 'diagnostico')
    return render(request, 'modulo/listar_estudiantes_tdah.html', {'estudiantes_tdah': estudiantes_tdah})



def detalle_estudiante_tdah(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    planificaciones = Planificacion.objects.filter(estudiante=estudiante)
    bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)

    context = {
        'estudiante': estudiante,
        'planificaciones': planificaciones,
        'bitacoras': bitacoras,
    }

    return render(request, 'modulo/detalle_estudiante_tdah.html', context)