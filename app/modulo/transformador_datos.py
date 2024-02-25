
import numpy as np
import pandas as pd

# Cargar datos iniciales de conductas_dataset
conductas_dataset = [66, 11, 63, 68, 96, 12, 26, 13, 58, 26, 11, 13, 18, 22, 74, 27, 33, 34, 108, 19, 10,
                      13, 53, 21, 33, 11, 12.5, 18.5, 31, 32.5, 24, 62.5, 23.5, 122]
avances_dataset = [97, 16.5, 89.5, 95, 139.5, 18, 36.5, 19, 77, 37.5, 16, 19, 27, 33, 92, 36, 45.5, 50.5, 
                   154, 27.5, 15, 19.5, 79.5, 31, 47, 15.5, 17.5, 22.5, 44.5, 44, 34, 87.5, 23.5, 180.5]
def transformar_datos(estudiante, bitacoras):
    global conducta_dataset, avance_dataset  # Indicar que se utilizarán las variables globales dentro de 
    #la función

    # Transformar el sexo
    sexo = 1 if estudiante.genero.upper() == 'M' else 0

    edad = estudiante.edad

    # Transformar las inasistencias (asistencias)
    inasistencias = bitacoras.filter(asistencias='No').count()

    # Calcular el total de terapias (sumar inasistencias)
    totalTerapias = sum([bitacora.observacion_conducta.count('excelente') +
                      bitacora.observacion_conducta.count('buena') +
                      bitacora.observacion_conducta.count('regular')
                      for bitacora in bitacoras])


    # Calcular la conducta
    total_excelente = sum([bitacora.observacion_conducta.count('excelente') for bitacora in bitacoras])
    total_buena = sum([bitacora.observacion_conducta.count('buena') for bitacora in bitacoras])
    total_regular = sum([bitacora.observacion_conducta.count('regular') for bitacora in bitacoras])

    conducta_ponderada = (total_excelente * 1.5) + (total_buena * 1) + (total_regular * 0.5)
    
    # Calcular los temas trabajados
    temas = ['m', 'vocales', 'fonemas', 'fonologia', 'escritura', 'p', 'lectura', 'dictado', 's', 'l', 'n', 
             'd', 'b', 't', 'g']
    temas_trabajados = {tema: 0 for tema in temas}
    
    # Iterar sobre cada bitácora en el conjunto
    for bitacora in bitacoras:
        # Separar los temas trabajados en una lista de letras
        temas_formulario = bitacora.temas_trabajados.replace(' ', '').lower().split(',')

        # Incrementar el contador solo para los temas que están en la lista 'temas'
        for tema in temas_formulario:
            tema = tema.strip()
            if tema in temas:
                temas_trabajados[tema] += 1

   # Imprimir resultados
    for tema, recuento in temas_trabajados.items():
        print(f'{tema}: {recuento}')
    # Calcular el avance
    avance_mejorando = sum([bitacora.avance.count('mejorando') for bitacora in bitacoras])
    avance_regular = sum([bitacora.avance.count('regular') for bitacora in bitacoras])
    avance_retroceso = sum([bitacora.avance.count('retroceso') for bitacora in bitacoras])

    avance_ponderado = (avance_mejorando * 1.5) + (avance_regular * 1) + (avance_retroceso * 0.5)

    avances_dataset.append(avance_ponderado)
    # Calcular la conducta total del niño actual

    # Agregar la conducta del niño actual a la lista de conductas del dataset
    conductas_dataset.append(conducta_ponderada)
    

    # Clasificar en categorías según cuartiles
    df = pd.DataFrame(conductas_dataset, columns=['Total'])
    q1 = df['Total'].quantile(0.25)
    q2 = df['Total'].median()
    q3 = df['Total'].quantile(0.75)
    conducta_total = pd.cut(df['Total'], bins=[float('-inf'), q1, q2, float('inf')], labels=['Bajo', 'Medio', 
                                                                                             'Alto']).values[-1]


    # Clasificar en categorías según cuartiles para avance
    df_avance = pd.DataFrame(avances_dataset, columns=['Total'])
    q1_avance = df_avance['Total'].quantile(0.25)
    q2_avance = df_avance['Total'].median()
    q3_avance = df_avance['Total'].quantile(0.75)
    avance_total = pd.cut(df_avance['Total'], bins=[float('-inf'), q1_avance, q2_avance, float('inf')],
                          labels=['Bajo', 'Medio', 'Alto']).values[-1]


    # Mapear las categorías a valores numéricos para avance
    mapeo_categorias_avance = {'Bajo': 1, 'Medio': 2, 'Alto': 3}
    avance = mapeo_categorias_avance[avance_total]

    # Mapear las categorías a valores numéricos
    mapeo_categorias = {'Bajo': 1, 'Medio': 2, 'Alto': 3}
    conducta = mapeo_categorias[conducta_total]
    
    # Crear el diccionario con los datos transformados
    datos_transformados = {
        'sexo': sexo,
        'edad': edad,
        'inasistencias': inasistencias,
        'totalTerapias': totalTerapias,
        'conducta': conducta,
        'avance': avance,
        **temas_trabajados
    }

    return datos_transformados


