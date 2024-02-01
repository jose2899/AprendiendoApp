from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico
from app.planificaciones.models import Planificacion
from app.bitacora.models import NuevaBitacora
from app.modulo.transformador_datos import transformar_datos
import joblib
import pandas as pd

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

modelo_optimizado = joblib.load('C:/Users/ANDRES RIOS/tesisModelo/modelo_optimizado_rf.pkl')

def predecir_avance_lectoescritura(request, estudiante_id):
    # Obtener el objeto Estudiante
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)

    if request.method == 'POST':
        # Extraer datos del formulario
        bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)

        # Llamar a transformar_datos con los argumentos adecuados
        datos_transformados = transformar_datos(estudiante, bitacoras)

        # Realizar la predicción con el modelo
        prediccion = modelo_optimizado.predict(pd.DataFrame([datos_transformados]))[0]

        # Devolver la predicción como una respuesta JSON
        return render(request, 'modulo/resultado_prediccion.html', {'prediccion': prediccion, 'estudiante': estudiante})

    # Si la solicitud no es POST, simplemente renderizar la página
    bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)
    return render(request, 'modulo/detalle_estudiante_tdah.html', {'estudiante': estudiante, 'bitacoras': bitacoras})

