from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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
import os
import joblib

import joblib
import pandas as pd

modelo_predeterminado_path = os.path.join(os.path.dirname(__file__), 'modelos/modelo_optimizado_rf.pkl')
# Cargar el modelo



def seleccionar_estudiante(request):
    estudiantes_tdah = Planificacion.objects.filter(diagnostico__nombre_diagnostico='TDAH', 
                                                    estudiante__edad__range=(7, 8)).select_related('estudiante', 'diagnostico')
    return render(request, 'modulo/fases_proceso.html', {'estudiantes_tdah': estudiantes_tdah})

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
    


def cargar_modelo(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    # Inicializar la variable modelo_optimizado
    if request.method == 'POST':
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
            mensaje_confirmacion = "El modelo se ha cargado correctamente."
            # Redirigir a alguna página de confirmación o a la siguiente fase
            return render(request, 'modulo/fases_proceso.html', {'mensaje_confirmacion': mensaje_confirmacion, 
                                                                 'form': form, 'estudiante': estudiante}) 
        else:
            # Si el formulario no es válido, devolver el formulario con un mensaje de error
            mensaje_error = "No se ha cargado ningún modelo. Por favor, cargue un modelo antes de continuar."
            return render(request, 'modulo/fases_proceso.html', {'form': form, 'estudiante': estudiante, 
                                                                 'mensaje_error': mensaje_error})
    else:
        # Si no, mostrar el formulario para cargar el modelo
        form = ModeloForm()
        request.session['modelo_path'] = modelo_predeterminado_path
        mensaje_confirmacion = "El modelo predeterminado se ha cargado correctamente."
        request.session['modelo_path'] = modelo_predeterminado_path
        return render(request, 'modulo/fases_proceso.html', {'form': form, 'estudiante': estudiante, 
                                                             'mensaje_confirmacion': mensaje_confirmacion})
    
umbrales = {
    'fonemas': {'min': 0, 'max': 3},
    'fonologia': {'min': 0, 'max': 3},
    'm': {'min': 1.5, 'max': 10},
    't':{'min': 0, 'max': 5},
    'd':{'min': 0, 'max': 7},
    'l':{'min': 0.50, 'max': 7},
    'n':{'min': 0, 'max': 5},
    'b':{'min': 0, 'max': 3},
    'g':{'min': 0, 'max': 2},
    'p':{'min': 1, 'max': 10},
    's':{'min': 0, 'max': 8},
    'dictado':{'min': 0.50, 'max': 16},
    'escritura': {'min': 0, 'max': 5},
    'lectura': {'min': 1.5, 'max': 15},
    'vocales': {'min': 1.5, 'max': 5},
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

        # Cargar el modelo
        try:
            modelo_optimizado = joblib.load(modelo_path)
        except Exception as e:
            return JsonResponse({'error': f'Error al cargar el modelo: {str(e)}'}, status=500)

        X_prueba = pd.DataFrame([datos_transformados]).drop('avanceLectoescritura', axis=1, errors='ignore')
        y_prueba = pd.DataFrame([datos_transformados]).get('avanceLectoescritura')

        try:
            # Realizar la predicción
            prediccion = modelo_optimizado.predict(X_prueba)
            importancias_temas = modelo_optimizado.feature_importances_
        except Exception as e:
            return JsonResponse({'error': f'Error en la predicción: {str(e)}'}, status=500)

        avance_predicho = prediccion[0]  # Obtener el nivel de avance predicho

        # Asignar el nivel de avance en formato de texto
        nivel_avance = 'alto' if avance_predicho == 'Alto' else 'medio' if avance_predicho == 'Medio' else 'bajo'

        # Calcular la importancia de cada tema
        temas_importancia = dict(zip(temas, importancias_temas))
        temas_ordenados = sorted(temas_importancia.keys(), key=lambda x: temas_importancia[x], reverse=True)

        # Seleccionar los temas más importantes a recomendar
        N_temas_importantes = 5
        temas_relevantes = temas_ordenados[:N_temas_importantes]

        # Controlar el avance de los temas según los umbrales
        temas_trabajados = {tema: min(datos_transformados.get(tema, 0), umbrales[tema]['max']) for tema in temas}

        # Determinar los temas a recomendar
        temas_a_recomendar = []
        if avance_predicho == 'Alto':
            for tema in temas_relevantes:
                if temas_trabajados[tema] < umbrales[tema]['max']:
                    temas_a_recomendar.append(tema)
        else:
            for tema in temas_relevantes:
                if temas_trabajados[tema] < umbrales[tema]['max']:
                    temas_a_recomendar.append(tema)
            if len(temas_a_recomendar) < N_temas_importantes:
                temas_con_umb_minimo = [tema for tema in temas if umbrales[tema]['max'] >= 1]
                adicionales_necesarios = N_temas_importantes - len(temas_a_recomendar)
                temas_adicionales = [tema for tema in temas_con_umb_minimo if tema not in temas_a_recomendar]
                temas_adicionales_seleccionados = temas_adicionales[:adicionales_necesarios]
                for tema in temas_adicionales_seleccionados:
                    if temas_trabajados[tema] < umbrales[tema]['max']:
                        temas_a_recomendar.append(tema)
        data = {
            'prediccion': prediccion.tolist(),  # Convertir a lista para serializar
            'temas_relevantes': temas_a_recomendar,
        }
        return JsonResponse(data)
    return render(request, 'modulo/fases_proceso.html', context)


def exportar_prediccion_pdf(request, estudiante_id):
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
        modelo_optimizado = joblib.load(modelo_path)
        X_prueba = pd.DataFrame([datos_transformados]).drop('avanceLectoescritura', axis=1)
        y_prueba = pd.DataFrame([datos_transformados]).get('avanceLectoescritura')
        # Realizar la predicción
        prediccion = modelo_optimizado.predict(X_prueba)
        avance_predicho = prediccion[0]  # Obtener el nivel de avance predicho

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
        temas_relevantes = temas_ordenados[:N_temas_importantes]

        # Controlar el avance de los temas según los umbrales
        temas_trabajados = {tema: min(datos_transformados.get(tema, 0), umbrales[tema]['max']) for tema in temas}

        # Determinar los temas a recomendar
        temas_a_recomendar = []
        if avance_predicho == 'Alto':
            for tema in temas_relevantes:
                if temas_trabajados[tema] < umbrales[tema]['max']:
                    temas_a_recomendar.append(tema)
        else:
            for tema in temas_relevantes:
                if temas_trabajados[tema] < umbrales[tema]['max']:
                    temas_a_recomendar.append(tema)
            if len(temas_a_recomendar) < N_temas_importantes:
                temas_con_umb_minimo = [tema for tema in temas if umbrales[tema]['max'] >= 1]
                adicionales_necesarios = N_temas_importantes - len(temas_a_recomendar)
                temas_adicionales = [tema for tema in temas_con_umb_minimo if tema not in temas_a_recomendar]
                temas_adicionales_seleccionados = temas_adicionales[:adicionales_necesarios]
                for tema in temas_adicionales_seleccionados:
                    if temas_trabajados[tema] < umbrales[tema]['max']:
                        temas_a_recomendar.append(tema)
        context['prediccion'] = prediccion.tolist()
        context['estudiante'] = estudiante
        context['temas_relevantes'] = temas_a_recomendar
        #context['precision_prueba'] = precision_prueba
        context['reporte_clasificacion'] = reporte_clasificacion
        context['matriz_confusion'] = matriz.tolist()
        response = PDFTemplateResponse(request=request,
                               template='modulo/resultado_prediccion.html',
                               filename=f'detalle_prediccion_{estudiante_id}.pdf',
                               context=context)
        return response

    return HttpResponse(status=405)
