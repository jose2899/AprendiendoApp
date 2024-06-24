from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
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

import joblib
import pandas as pd

modelo_predeterminado = joblib.load('C:/Users/ANDRES RIOS/tesisModelo/modelo_optimizado_rf.pkl')


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
        # Agregar la información de la predicción al contexto
        transformacion_exitosa = True
        # Almacenar los datos transformados en la sesión
        request.session['datos_transformados'] = datos_transformados
        print("se realizo la transformacion")
        mensaje_confirmacion = "Se ha transformado correctamente."
        context['mensaje_confirmacion'] = mensaje_confirmacion
        response_data = {
            'transformacion_exitosa': transformacion_exitosa,
            # Puedes incluir más datos en la respuesta si los necesitas
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
            nombre_archivo = modelo_pkl.name  # Obtener el nombre del archivo subido por el usuario
            with open(nombre_archivo, 'wb') as f:
                for chunk in modelo_pkl.chunks():
                    f.write(chunk)
            # Guardar la ruta del archivo del modelo en la sesión
            request.session['modelo_path'] = nombre_archivo
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
        mensaje_confirmacion = "El modelo predeterminado se ha cargado correctamente."
        modelo_predeterminado_path = 'C:/Users/ANDRES RIOS/tesisModelo/modelo_optimizado_rf.pkl'
        request.session['modelo_path'] = modelo_predeterminado_path
        return render(request, 'modulo/fases_proceso.html', {'form': form, 'estudiante': estudiante, 
                                                             'mensaje_confirmacion': mensaje_confirmacion})
    

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
        modelo_optimizado = joblib.load(modelo_path)
        X_prueba = pd.DataFrame([datos_transformados]).drop('avanceLectoescritura', axis=1)
        y_prueba = pd.DataFrame([datos_transformados]).get('avanceLectoescritura')
        # Realizar la predicción
        prediccion = modelo_optimizado.predict(X_prueba)
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
        
        data = {
            'prediccion': prediccion.tolist(),  # Convertir a lista para serializar
            'temas_relevantes': temas_relevantes,
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
        N_temas_importantes = 8
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
