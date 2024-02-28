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

import joblib
import pandas as pd

modelo_optimizado = joblib.load('C:/Users/ANDRES RIOS/tesisModelo/modelo_optimizado_rf.pkl')


def seleccionar_estudiante(request):
    estudiantes_tdah = Planificacion.objects.filter(diagnostico__nombre_diagnostico='TDAH', estudiante__edad__range=(7, 8)).select_related('estudiante', 'diagnostico')
    return render(request, 'modulo/fases_proceso.html', {'estudiantes_tdah': estudiantes_tdah})

def transformar_datosF(request, estudiante_id):
    transformacion_exitosa = False
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
    print("se realizo la transformacion")
    context['transformacion_exitosa'] = transformacion_exitosa
    return render(request, 'modulo/fases_proceso.html', context)
    


def cargar_modelo(request, estudiante_id):
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    # Inicializar la variable modelo_optimizado
    modelo_optimizado = None

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

            # Cargar el modelo que ha sido subido por el usuario
            modelo_optimizado = joblib.load(nombre_archivo)
            # Mostrar un mensaje de confirmación
            mensaje_confirmacion = "El modelo se ha cargado correctamente."
            # Redirigir a alguna página de confirmación o a la siguiente fase
            return render(request, 'modulo/fases_proceso.html', {'mensaje_confirmacion': mensaje_confirmacion, 'form': form})  # Cambia esta ruta
    else:
        # Si no, mostrar el formulario para cargar el modelo
        form = ModeloForm()
    
    # Siempre cargar el modelo (tanto el predeterminado como el cargado por el usuario)
    modelo_optimizado = joblib.load('C:/Users/ANDRES RIOS/tesisModelo/modelo_optimizado_rf.pkl')

    # Lógica para realizar la predicción con el modelo
    # ...

    # Renderizar el template con el formulario y otros datos necesarios
    return render(request, 'modulo/fases_proceso.html', {'form': form, 'estudiante': estudiante} )

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
        # Lógica para realizar la predicción
        datos_transformados = transformar_datos(estudiante, bitacoras)
        prediccion = modelo_optimizado.predict(pd.DataFrame([datos_transformados]))[0]
        # Obtengo la importancia de las características (temas) del modelo
        importancias_temas = modelo_optimizado.feature_importances_
        temas = ['m', 'vocales', 'fonemas', 'fonologia', 'escritura', 'p', 'lectura', 'dictado', 's', 'l', 
                        'n', 'd', 'b', 't', 'g']
        temas_importancia = dict(zip(temas, importancias_temas))
        temas_ordenados = sorted(temas_importancia.keys(), key=lambda x: temas_importancia[x], reverse=True)
        N_temas_importantes = 5
        temas_relevantes = temas_ordenados[:N_temas_importantes]

        print("Importancia de las características (temas):")
        for tema in temas_relevantes:
            importancia = temas_importancia[tema]
            print(f"{tema}: {importancia}")

        data = {
        'prediccion': prediccion,
        'temas_relevantes': temas_relevantes,
        }
        return JsonResponse(data)
    
    return render(request, 'modulo/fases_proceso.html', context)