from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from app.usuarios.usuario.models import Estudiante
from app.terapiass.models import Diagnostico
from app.planificaciones.models import Planificacion
from app.bitacora.models import NuevaBitacora
from app.modulo.transformador_datos import transformar_datos
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


import joblib
import pandas as pd

modelo_optimizado = joblib.load('C:/Users/ANDRES RIOS/tesisModelo/modelo_optimizado_rf.pkl')


def detalle_estudiante_tdah(request, estudiante_id = None):
    if estudiante_id:
        estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
        planificaciones = Planificacion.objects.filter(estudiante=estudiante)
        bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)
        
        context = {
            'estudiante': estudiante,
            'planificaciones': planificaciones,
            'bitacoras': bitacoras,
        }

        if request.method == 'POST':
            # Extraer datos del formulario
            bitacoras = NuevaBitacora.objects.filter(bitacora__estudiante=estudiante)

            # Llamar a transformar_datos con los argumentos adecuados
            datos_transformados = transformar_datos(estudiante, bitacoras)

            # Realizar la predicción con el modelo
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

            # Agregar la información de la predicción al contexto
            context.update({'prediccion': prediccion, 'temas_relevantes': temas_relevantes})
            

        return render(request, 'modulo/fases_proceso.html', context)
    else:
        estudiantes_tdah = Planificacion.objects.filter(diagnostico__nombre_diagnostico='TDAH', estudiante__edad__range=(7, 8)).select_related('estudiante', 'diagnostico')
        return render(request, 'modulo/fases_proceso.html', {'estudiantes_tdah': estudiantes_tdah})
