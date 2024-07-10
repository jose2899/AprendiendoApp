from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico
from app.planificaciones.models import Planificacion
from app.bitacora.models import NuevaBitacora
from app.modulo.transformador_datos import transformar_datos
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from app.modulo.forms import ModeloForm
from sklearn.metrics import classification_report
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from weasyprint import HTML
from django.template.loader import render_to_string
import joblib
import traceback
import joblib
import pandas as pd

modelo_predeterminado_path = os.path.join(os.path.dirname(__file__), 'modelos/modelo_optimizado_rf.pkl')
# Cargar el modelo



def seleccionar_estudiante(request):
    search_query = request.GET.get('q', '')  # Obtener el término de búsqueda de los parámetros de la URL
    estudiantes_tdah = Planificacion.objects.filter(
        diagnostico__nombre_diagnostico='TDAH', 
        estudiante__edad__range=(7, 8)).select_related('estudiante', 'diagnostico')
    if search_query:
        estudiantes_tdah = estudiantes_tdah.filter(estudiante__nombre_completo__icontains=search_query)

    return render(request, 'modulo/fases_proceso.html', {'estudiantes_tdah': estudiantes_tdah, 'search_query': search_query})

def transformar_datosF(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    planificaciones = Planificacion.objects.filter(estudiante=estudiante)
    bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)
    transformacion_exitosa = False
    context = {
            'estudiante': estudiante,
            'planificaciones': planificaciones,
            'bitacoras': bitacoras,
        }
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        
        # Llamar a transformar_datos con los argumentos adecuados
        datos_transformados = transformar_datos(estudiante, bitacoras)
        transformacion_exitosa = True
        # Almacenar los datos transformados en la sesión
        request.session['datos_transformados'] = datos_transformados
        print("se realizo la transformacion")
        mensaje_confirmacion = "Se ha transformado correctamente."
        context['mensaje_confirmacion'] = mensaje_confirmacion
        response_data = {
            'transformacion_exitosa': transformacion_exitosa,
            }
        return JsonResponse(response_data)
    context['transformacion_exitosa'] = transformacion_exitosa
    return render(request, 'modulo/fases_proceso.html', context)
    

@login_required
def cargar_modelo(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    # Inicializar la variable modelo_optimizado
    if request.method == 'POST':
        if not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para cargar un modelo.')
            return render(request, 'modulo/fases_proceso.html', {'estudiante': estudiante})
        # Si el formulario ha sido enviado, procesarlo
        form = ModeloForm(request.POST, request.FILES)
        if form.is_valid():
            # Si el formulario es válido, guardar el archivo del modelo
            modelo_pkl = request.FILES['modelo_pkl']
            modelo_path = os.path.join('modelos', modelo_pkl.name) # Obtener el nombre del archivo subido por el usuario
            with open(modelo_path, 'wb') as f:
                for chunk in modelo_pkl.chunks():
                    f.write(chunk)
            # Guardar la ruta del archivo del modelo en la sesión
            request.session['modelo_path'] = modelo_path
            messages.success(request, 'El modelo se cargo correctamente.')
            # Redirigir a alguna página de confirmación o a la siguiente fase
            return render(request, 'modulo/fases_proceso.html', {'form': form, 'estudiante': estudiante}) 
        else:
            # Si el formulario no es válido, devolver el formulario con un mensaje de error
            messages.error(request, f'El modelo no se cargo correctamente')
            return render(request, 'modulo/fases_proceso.html', {'form': form, 'estudiante': estudiante})
    else:
        # Si no, mostrar el formulario para cargar el modelo
        form = ModeloForm()
        request.session['modelo_path'] = modelo_predeterminado_path
        messages.success(request, 'El modelo predeterminado se cargo correctamente.')
        request.session['modelo_path'] = modelo_predeterminado_path
        return render(request, 'modulo/fases_proceso.html', {'form': form, 'estudiante': estudiante})
    
umbrales = {
    'fonemas': {'min': 0, 'max': 4},
    'fonologia': {'min': 0, 'max': 4},
    'm': {'min': 1.5, 'max': 8},
    't':{'min': 0, 'max': 3},
    'd':{'min': 0, 'max': 4},
    'l':{'min': 0.50, 'max': 5},
    'n':{'min': 0, 'max': 4},
    'b':{'min': 0, 'max': 2},
    'g':{'min': 0, 'max': 1},
    'p':{'min': 1, 'max': 6},
    's':{'min': 0, 'max': 5},
    'dictado':{'min': 0.50, 'max': 10},
    'escritura': {'min': 0, 'max': 4},
    'lectura': {'min': 1.5, 'max': 10},
    'vocales': {'min': 1.5, 'max': 4},
}
temas = ['m', 'vocales', 'fonemas', 'fonologia', 'escritura', 'p', 'lectura', 'dictado', 's', 'l', 
                     'n', 'd', 'b', 't', 'g']

def realizar_prediccion(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    planificaciones = Planificacion.objects.filter(estudiante=estudiante)
    bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)
    context = {
            'estudiante': estudiante,
            'planificaciones': planificaciones,
            'bitacoras': bitacoras,
        }

    if request.method == 'POST':

        # Obtener los datos transformados de la sesión
        datos_transformados = request.session.get('datos_transformados')
        modelo_path = request.session.get('modelo_path')

        if not datos_transformados or not modelo_path:
            return JsonResponse({'error': 'Datos de sesión no encontrados'}, status=400)
        
        modelo_optimizado = joblib.load(modelo_path)

        X_prueba = pd.DataFrame([datos_transformados]).drop('avanceLectoescritura', axis=1)
        y_prueba = pd.DataFrame([datos_transformados]).get('avanceLectoescritura')
           
        prediccion = modelo_optimizado.predict(X_prueba)
        importancias_temas = modelo_optimizado.feature_importances_

        # Calcular la importancia de cada tema
        temas_importancia = dict(zip(temas, importancias_temas))
        temas_ordenados = sorted(temas_importancia.keys(), key=lambda x: temas_importancia[x], reverse=True)

        avance_predicho = prediccion[0]  # Obtener el nivel de avance predicho

        # Seleccionar los temas más importantes a recomendar
        N_temas_importantes = 5
        temas_relevantes = temas_ordenados[:N_temas_importantes]

        # Controlar el avance de los temas según los umbrales
        temas_trabajados = {tema: min(datos_transformados.get(tema, 0), umbrales[tema]['max']) for tema in temas}
        precision_prueba = accuracy_score([y_prueba], [prediccion])

        # Determinar los temas a recomendar
        # Calcular sesiones faltantes y promedio de sesiones restantes
        sesiones_faltantes = {}
        total_sesiones_restantes = 0
        temas_a_recomendar = []
        promedio_sesiones_restantes = 0
        if avance_predicho != "Alto":
            for tema in temas_relevantes:
                faltantes = max(umbrales[tema]['max'] - temas_trabajados[tema], 0)
                sesiones_faltantes[tema] = faltantes
                total_sesiones_restantes += faltantes
                if temas_trabajados[tema] < umbrales[tema]['max']:
                    temas_a_recomendar.append(tema)

            promedio_sesiones_restantes = total_sesiones_restantes / len(temas_relevantes) if temas_relevantes else 0
            promedio_sesiones_restantes = round(promedio_sesiones_restantes)
            
            if len(temas_a_recomendar) < N_temas_importantes:
                temas_con_umb_minimo = [tema for tema in temas if umbrales[tema]['max'] >= 1]
                adicionales_necesarios = N_temas_importantes - len(temas_a_recomendar)
                temas_adicionales = [tema for tema in temas_con_umb_minimo if tema not in temas_a_recomendar]
                temas_adicionales_seleccionados = temas_adicionales[:adicionales_necesarios]

                for tema in temas_adicionales_seleccionados:
                    faltantes = max(umbrales[tema]['max'] - temas_trabajados[tema], 0)
                    sesiones_faltantes[tema] = faltantes
                    total_sesiones_restantes += faltantes

                    if temas_trabajados[tema] < umbrales[tema]['max']:
                        temas_a_recomendar.append(tema)

                promedio_sesiones_restantes = total_sesiones_restantes / len(temas_relevantes) if temas_relevantes else 0
                promedio_sesiones_restantes = round(promedio_sesiones_restantes) 

        data = {
            'prediccion': prediccion.tolist(),  # Convertir a lista para serializar
            'temas_relevantes': temas_a_recomendar,
            'sesiones_faltantes': sesiones_faltantes,
            'promedio_sesiones_restantes': promedio_sesiones_restantes,
        }
        print('la precision es', precision_prueba)
        return JsonResponse(data)
    return render(request, 'modulo/fases_proceso.html', context)

"""
def exportar_prediccion_pdf(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    planificaciones = Planificacion.objects.filter(estudiante=estudiante)
    bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)
    context = {
            'estudiante': estudiante,
            'planificaciones': planificaciones,
            'bitacoras': bitacoras,
        }

    if request.method == 'GET':
        # Obtener los datos transformados de la sesión
        datos_transformados = request.session.get('datos_transformados')
            
        modelo_path = request.session.get('modelo_path')
        modelo_optimizado = joblib.load(modelo_path)
        X_prueba = pd.DataFrame([datos_transformados]).drop('avanceLectoescritura', axis=1)
        y_prueba = pd.DataFrame([datos_transformados]).get('avanceLectoescritura')
        # Realizar la predicción
        prediccion = modelo_optimizado.predict(X_prueba)
        precision_prueba = accuracy_score([y_prueba], [prediccion])
        # Calcular el reporte de clasificación
        reporte_clasificacion = classification_report([y_prueba], [prediccion], zero_division=1)
        # Imprimir el informe de clasificación en la consola
        matriz = confusion_matrix(y_prueba, prediccion)
        importancias_temas = modelo_optimizado.feature_importances_
        temas = ['m', 'vocales', 'fonemas', 'fonologia', 'escritura', 'p', 'lectura', 'dictado', 's', 'l', 
                            'n', 'd', 'b', 't', 'g']
        temas_importancia = dict(zip(temas, importancias_temas))
        temas_ordenados = sorted(temas_importancia.keys(), key=lambda x: temas_importancia[x], reverse=True)
        N_temas_importantes = 5
        temas_relevantesE = temas_ordenados[:N_temas_importantes]
        temas_trabajados = {tema: datos_transformados.get(tema, 0) for tema in temas}
        temas_relevantes = [tema for tema in temas_relevantesE if temas_trabajados[tema] == 0]
        for tema in temas_relevantes:
            importancia = temas_importancia[tema]
            print(f"{tema}: {importancia}")        
        context['prediccion'] = prediccion.tolist()
        context['estudiante'] = estudiante
        context['temas_relevantes'] = temas_relevantes
        context['precision_prueba'] = precision_prueba
        context['reporte_clasificacion'] = reporte_clasificacion
        context['matriz_confusion'] = matriz.tolist()
        return PDFTemplateResponse(request=request,
                               template='modulo/resultado_prediccion.html',
                               filename=f'detalle_prediccion_{estudiante_id}.pdf',
                               context=context)

    return render(request, 'modulo/fases_proceso.html', context)
"""


#despliegue

@csrf_exempt
def exportar_prediccion_pdf(request, estudiante_id):
    try:
        estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
        planificaciones = Planificacion.objects.filter(estudiante=estudiante)
        bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)
        context = {
            'estudiante': estudiante,
            'planificaciones': planificaciones,
            'bitacoras': bitacoras,
        }

        if request.method == 'POST':
            datos_transformados = request.session.get('datos_transformados')
            modelo_path = request.session.get('modelo_path')

            if not datos_transformados or not modelo_path:
                return JsonResponse({'error': 'Datos de sesión no encontrados'}, status=400)

            modelo_optimizado = joblib.load(modelo_path)

            X_prueba = pd.DataFrame([datos_transformados]).drop('avanceLectoescritura', axis=1)
            y_prueba = pd.DataFrame([datos_transformados]).get('avanceLectoescritura')

            prediccion = modelo_optimizado.predict(X_prueba)
            importancias_temas = modelo_optimizado.feature_importances_


            # Calcular la importancia de cada tema
            temas_importancia = dict(zip(temas, importancias_temas))
            temas_ordenados = sorted(temas_importancia.keys(), key=lambda x: temas_importancia[x], reverse=True)

            avance_predicho = prediccion[0]  # Obtener el nivel de avance predicho

            # Seleccionar los temas más importantes a recomendar
            N_temas_importantes = 5
            temas_relevantes = temas_ordenados[:N_temas_importantes]

            # Controlar el avance de los temas según los umbrales
            temas_trabajados = {tema: min(datos_transformados.get(tema, 0), umbrales[tema]['max']) for tema in temas}
            precision_prueba = accuracy_score([y_prueba], [prediccion])
            reporte_clasificacion = classification_report([y_prueba], [prediccion], zero_division=1)

            # Determinar los temas a recomendar
            sesiones_faltantes = {}
            total_sesiones_restantes = 0
            temas_a_recomendar = []
            promedio_sesiones_restantes = 0
            if avance_predicho != "Alto":
                for tema in temas_relevantes:
                    faltantes = max(umbrales[tema]['max'] - temas_trabajados[tema], 0)
                    sesiones_faltantes[tema] = faltantes
                    total_sesiones_restantes += faltantes
                    if temas_trabajados[tema] < umbrales[tema]['max']:
                        temas_a_recomendar.append(tema)

                promedio_sesiones_restantes = total_sesiones_restantes / len(temas_relevantes) if temas_relevantes else 0
                promedio_sesiones_restantes = round(promedio_sesiones_restantes)

                if len(temas_a_recomendar) < N_temas_importantes:
                    temas_con_umb_minimo = [tema for tema in temas if umbrales[tema]['max'] >= 1]
                    adicionales_necesarios = N_temas_importantes - len(temas_a_recomendar)
                    temas_adicionales = [tema for tema in temas_con_umb_minimo if tema not in temas_a_recomendar]
                    temas_adicionales_seleccionados = temas_adicionales[:adicionales_necesarios]

                    for tema in temas_adicionales_seleccionados:
                        faltantes = max(umbrales[tema]['max'] - temas_trabajados[tema], 0)
                        sesiones_faltantes[tema] = faltantes
                        total_sesiones_restantes += faltantes

                        if temas_trabajados[tema] < umbrales[tema]['max']:
                            temas_a_recomendar.append(tema)

                    promedio_sesiones_restantes = total_sesiones_restantes / len(temas_relevantes) if temas_relevantes else 0
                    promedio_sesiones_restantes = round(promedio_sesiones_restantes)

            context['prediccion'] = prediccion.tolist()
            context['temas_relevantes'] = temas_a_recomendar
            context['sesiones_faltantes'] = sesiones_faltantes
            context['promedio_sesiones_restantes'] = promedio_sesiones_restantes
            context['precision_prueba'] = precision_prueba
            context['reporte_clasificacion'] = reporte_clasificacion

            html_string = render_to_string('modulo/resultado_prediccion.html', context)
            pdf_file = HTML(string=html_string).write_pdf()

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="detalle_prediccion_{estudiante_id}.pdf"'
            return response

        return JsonResponse({'error': 'Método no permitido'}, status=405)

    except Exception as e:
        print(traceback.format_exc())  # Esto imprimirá el error completo en los logs
        return JsonResponse({'error': 'Ocurrió un error interno en el servidor.'}, status=500)

