from django.shortcuts import render
from app.usuarios.usuario.models import Estudiante
from app.usuarios.adminis.models import Adminis
from app.bitacora.models import Bitacora
from django.db.models import Count
from collections import Counter
from django.db.models.functions import ExtractMonth
from app.planificaciones.models import Planificacion
from app.usuarios.psicologo.models import Psicologo

# Create your views here.
def index(request):
    query = request.GET.get('q')

    total_estudiantes = Estudiante.objects.all().count()
    total_adminis = Adminis.objects.all().count()
    total_bitacora = Bitacora.objects.all().count()

    # Calcular el total de niños registrados por mes
    estudian_por_mes = Estudiante.objects.annotate(mes=ExtractMonth('fecha')).values('mes').annotate(total=Count('id')).order_by('mes')

    # Obtener los últimos 4 niños registrados
    ultimos_estudi = Estudiante.objects.order_by('-fecha')[:4]
    
    # Obtener todos los diagnósticos de todas las planificaciones
    diagnósticos = Planificacion.objects.values_list('diagnostico__nombre_diagnostico', flat=True)
    # Contar cuántas veces aparece cada diagnóstico
    conteo_diagnósticos = Counter(diagnósticos)

    # Ordenar los diagnósticos por la cantidad de veces que aparecen (de mayor a menor)
    diagnósticos_ordenados = conteo_diagnósticos.most_common()

    # Obtener los últimos 4 psicólogos agregados
    primeros_psicologos = Psicologo.objects.all()[:4]

    # Filtrar resultados si hay una consulta de búsqueda
    if query:
        # Realizar la búsqueda en los modelos relevantes
        resultados_estudiantes = Estudiante.objects.filter(nombre__icontains=query)
        resultados_admins = Adminis.objects.filter(nombre__icontains=query)
        resultados_psicologos = Psicologo.objects.filter(nombre__icontains=query)

        return render(request, 'home.html', {'resultados_estudiantes': resultados_estudiantes,
                                              'resultados_admins': resultados_admins,
                                              'resultados_psicologos': resultados_psicologos,
                                              'query': query})

    return render(request, 'home.html', {'total_estudiantes': total_estudiantes, 
                                          'total_admins': total_adminis, 
                                          'total_bitacora': total_bitacora, 
                                          'estudian_por_mes': estudian_por_mes, 
                                          'ultimos_estudi': ultimos_estudi, 
                                          'diagnósticos_ordenados': diagnósticos_ordenados, 
                                          'primeros_psicologos': primeros_psicologos})
