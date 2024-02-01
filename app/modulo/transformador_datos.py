import numpy as np
import pandas as pd

# Cargar datos iniciales de conductas_dataset (puedes modificar estos valores)
conductas_dataset = [66, 11, 63, 68, 96, 12, 26, 13, 58, 26, 11, 13, 18, 22, 74, 27, 33, 34, 108, 19, 10, 13, 53, 21, 33, 11, 12.5, 18.5, 31, 32.5, 24, 62.5, 23.5, 122, 22.5, 10, 84, 75.5, 9, 49, 9, 5, 6]
avances_dataset = [97, 16.5, 89.5, 95, 139.5, 18, 36.5, 19, 77, 37.5, 16, 19, 27, 33, 92, 36, 45.5, 50.5, 154, 27.5, 15, 19.5, 79.5, 31, 47, 15.5, 17.5, 22.5, 44.5, 44, 34, 87.5, 23.5, 180.5, 25.5, 14.5, 89.5, 94, 13.5, 73, 13, 6.5, 6]
def transformar_datos(estudiante, bitacoras):
    global conducta_dataset, avance_dataset  # Indicar que se utilizarán las variables globales dentro de la función

    # Transformar el sexo
    sexo = 1 if estudiante.genero.upper() == 'M' else 0
    print('genero', sexo)

    # Transformar las inasistencias (asistencias)
    inasistencias = bitacoras.filter(asistencias='No').count()
    print('---------asistenciassss ------------', inasistencias)
    # Calcular el total de terapias (sumar inasistencias)
    total_terapias = sum([bitacora.observacion_conducta.count('excelente') +
                      bitacora.observacion_conducta.count('buena') +
                      bitacora.observacion_conducta.count('regular')
                      for bitacora in bitacoras])

    print('---------total terapia ------------',total_terapias)

    # Calcular la conducta
    total_excelente = sum([bitacora.observacion_conducta.count('excelente') for bitacora in bitacoras])
    total_buena = sum([bitacora.observacion_conducta.count('buena') for bitacora in bitacoras])
    total_regular = sum([bitacora.observacion_conducta.count('regular') for bitacora in bitacoras])

    conducta = (total_excelente * 1.5) + (total_buena * 1) + (total_regular * 0.5)
    
    print('---------total conducta ------------',conducta)
    # Calcular los temas trabajados
    temas_trabajados = {}
    temas = ['m', 'vocales', 'fonemas', 'fonologia', 'escritura', 'p', 'lectura', 'dictado', 's', 'l', 'n', 'd', 'b', 't', 'g']
    
    for tema in temas:
        temas_trabajados[tema] = 0


    # Iterar sobre cada bitacora en el conjunto de consultas (QuerySet)
    for bitacora in bitacoras:
    # Separar los temas trabajados en una lista de letras
        temas_formulario = bitacora.temas_trabajados.replace(' ', '').lower().split(',')
    
        for tema in temas_formulario:
            tema = tema.strip()
            if tema in temas:
                temas_trabajados[tema] += 1
    
    print('---------temas ------------',temas_trabajados)
    # Calcular el avance
    avance_mejorando = sum([bitacora.avance.count('mejorando') for bitacora in bitacoras])
    avance_regular = sum([bitacora.avance.count('regular') for bitacora in bitacoras])
    avance_retroceso = sum([bitacora.avance.count('retroceso') for bitacora in bitacoras])

    avance = (avance_mejorando * 1.5) + (avance_regular * 1) + (avance_retroceso * 0.5)

    print('---------total avance ------------',avance)
    avances_dataset.append(avance)
    # Calcular la conducta total del niño actual

    # Agregar la conducta del niño actual a la lista de conductas del dataset
    conductas_dataset.append(conducta)
    

    # Clasificar en categorías según cuartiles
    df = pd.DataFrame(conductas_dataset, columns=['Total'])
    q1 = df['Total'].quantile(0.25)
    q2 = df['Total'].median()
    q3 = df['Total'].quantile(0.75)
    categoria_conducta = pd.cut(df['Total'], bins=[float('-inf'), q1, q2, float('inf')], labels=['Bajo', 'Medio', 'Alto']).values[-1]

    print('---------categoria de la conducta ------------',categoria_conducta)

    # Clasificar en categorías según cuartiles para avance
    df_avance = pd.DataFrame(avances_dataset, columns=['Total'])
    q1_avance = df_avance['Total'].quantile(0.25)
    q2_avance = df_avance['Total'].median()
    q3_avance = df_avance['Total'].quantile(0.75)
    categoria_avance = pd.cut(df_avance['Total'], bins=[float('-inf'), q1_avance, q2_avance, float('inf')],labels=['Bajo', 'Medio', 'Alto']).values[-1]
    
    print('---------categoria avance ------------',categoria_avance)

    # Mapear las categorías a valores numéricos para avance
    mapeo_categorias_avance = {'Bajo': 1, 'Medio': 2, 'Alto': 3}
    valor_categoria_avance = mapeo_categorias_avance[categoria_avance]

    print('---------valor del avance ------------',valor_categoria_avance)

    # Mapear las categorías a valores numéricos
    mapeo_categorias = {'Bajo': 1, 'Medio': 2, 'Alto': 3}
    conducta_final = mapeo_categorias[categoria_conducta]
    
    print('---------valor conducta ------------',conducta_final)
    # Crear el diccionario con los datos transformados
    datos_transformados = {
        'sexo': sexo,
        'edad': estudiante.edad['edad'],
        'inasistencias': inasistencias,
        'total_terapias': total_terapias,
        'conducta': conducta,
        'avance': avance,
        'temas_trabajados': temas_trabajados,
        'categoria_conducta': categoria_conducta,  # Nueva variable
        'categoria_avance': categoria_avance,
        'conducta_final': conducta_final,
        'valor_categoria_avance': valor_categoria_avance,
        # Agrega otras variables aquí según sea necesario
    }

    return datos_transformados

# Resto del código del programa...
