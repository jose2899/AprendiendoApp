
import numpy as np
import pandas as pd
import re
import unicodedata
umbrales_maximos = {
    'm': 8,
    'vocales': 4,    
    'fonemas': 4,
    'fonologia': 4,
    'escritura': 4,
    'p': 6,
    'lectura': 10,
    'dictado': 10,
    's': 5,
    'l': 5,
    'n': 4,
    'd': 4,
    'b': 2,
    't': 3,
    'g': 1,
}

# Cargar datos iniciales de conductas_dataset
conductas_dataset = [66, 11, 63, 68, 96, 12, 26, 13, 58, 26, 11, 13, 18, 22, 74, 27, 33, 34, 108, 19, 10,
                      13, 53, 21, 33, 11, 12.5, 18.5, 31, 32.5, 24, 62.5, 23.5, 122]
avances_dataset = [97, 16.5, 89.5, 95, 139.5, 18, 36.5, 19, 77, 37.5, 16, 19, 27, 33, 92, 36, 45.5, 50.5, 
                   154, 27.5, 15, 19.5, 79.5, 31, 47, 15.5, 17.5, 22.5, 44.5, 44, 34, 87.5, 23.5, 180.5]

lecto_dataset = [416, 50.5, 405.5, 352, 528.5, 55, 115.5, 88, 291, 156.5, 90, 101, 98, 166, 347, 114, 138.5,
                  248.5, 572, 74.5, 103, 120.5, 245.5, 82, 161, 47.5, 70, 115, 169.5, 158.5, 171, 302, 109, 743.5]

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
    
       #conducta del niño tomando toda
   # Calcular la conducta
    total_excelente = sum([bitacora.observacion_conducta.count('excelente') for bitacora in bitacoras])
    total_buena = sum([bitacora.observacion_conducta.count('buena') for bitacora in bitacoras])
    total_regular = sum([bitacora.observacion_conducta.count('regular') for bitacora in bitacoras])

    conducta_ponderada = (total_excelente * 1.5) + (total_buena * 1) + (total_regular * 0.5)


    temas = ['m', 'vocales', 'fonemas', 'fonologia', 'escritura', 'p', 'lectura', 'dictado', 's', 'l', 'n', 
             'd', 'b', 't', 'g']
    
    temas_trabajados = {tema: 0 for tema in temas}
    bitacoras_contadas = {tema: [] for tema in temas}
    numero_temas = 0

    def eliminar_tildes(texto):
        # Normalizar el texto en forma de descomposición
        texto_normalizado = unicodedata.normalize('NFD', texto)
        # Filtrar los caracteres de acentuación
        texto_sin_tildes = ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn')
        return texto_sin_tildes


    for bitacora in bitacoras:
        # Utilizar una expresión regular para separar las palabras y mantener las letras
        temas_formulario = re.findall(r'\b\w+\b', bitacora.temas_trabajados.lower())

        for tema in temas_formulario:
            tema = eliminar_tildes(tema.strip())
            if tema in temas_trabajados and temas_trabajados[tema] < umbrales_maximos[tema]:
                temas_trabajados[tema] += 1
                bitacoras_contadas[tema].append(bitacora)
                numero_temas +=1

    """
    # Calcular la conducta
    # Calcular la conducta ponderada
    conducta_ponderada = 0
    for tema, maximo in umbrales_maximos.items():
        bitacoras_dentro_umbral = bitacoras_contadas[tema][:maximo]
        total_excelente = sum(
            bitacora.observacion_conducta.count('excelente') for bitacora in bitacoras_dentro_umbral
        )
        total_buena = sum(
            bitacora.observacion_conducta.count('buena') for bitacora in bitacoras_dentro_umbral
        )
        total_regular = sum(
            bitacora.observacion_conducta.count('regular') for bitacora in bitacoras_dentro_umbral
        )
        conducta_ponderada += (total_excelente * 1.5) + (total_buena * 1) + (total_regular * 0.5)
    """

   
   # Imprimir resultados
    for tema, recuento in temas_trabajados.items():
        print(f'{tema}: {recuento}')
    
    """
    #calcular el avance del niño pero solo si se pasa del umbral
    avance_ponderado = 0
    for tema, maximo in umbrales_maximos.items():
        bitacoras_dentro_umbral = bitacoras_contadas[tema][:maximo]
        total_mejorando = sum(
            bitacora.avance.count('mejorando') for bitacora in bitacoras_dentro_umbral
        )
        total_regular = sum(
            bitacora.avance.count('regular') for bitacora in bitacoras_dentro_umbral
        )
        total_retroceso = sum(
            bitacora.avance.count('retroceso') for bitacora in bitacoras_dentro_umbral
        )
        avance_ponderado += (total_mejorando * 1.5) + (total_regular * 1) + (total_retroceso * 0.5)
    """
     # calcular avance lecto
    #avance de todo el niño
    # Calcular el avance
    avance_mejorando = sum([bitacora.avance.count('mejorando') for bitacora in bitacoras])
    avance_regular = sum([bitacora.avance.count('regular') for bitacora in bitacoras])
    avance_retroceso = sum([bitacora.avance.count('retroceso') for bitacora in bitacoras])

    avance_ponderado = (avance_mejorando * 1.5) + (avance_regular * 1) + (avance_retroceso * 0.5)
    
    num_avance_lecto = 0
    num_avance_lecto = (conducta_ponderada + avance_ponderado + numero_temas + totalTerapias) - inasistencias
    print ('avance de la lectoescritura', num_avance_lecto)
    
    

    avances_dataset.append(avance_ponderado)
    # Calcular la conducta total del niño actual

    # Agregar la conducta del niño actual a la lista de conductas del dataset
    conductas_dataset.append(conducta_ponderada)
    lecto_dataset.append(num_avance_lecto)
    
    # Clasificar en categorías según cuartiles
    df = pd.DataFrame(conductas_dataset, columns=['Total'])
    q1 = df['Total'].quantile(0.25)
    q2 = df['Total'].median()
    q3 = df['Total'].quantile(0.75)
    conducta_total = pd.cut(df['Total'], bins=[float('-inf'), q1, q2, float('inf')], labels=['Bajo', 'Medio', 
                                                                                             'Alto']).values[-1]
    print("la condicta es", conducta_total)
    


    # Clasificar en categorías según cuartiles para avance
    df_avance = pd.DataFrame(avances_dataset, columns=['Total'])
    q1_avance = df_avance['Total'].quantile(0.25)
    q2_avance = df_avance['Total'].median()
    q3_avance = df_avance['Total'].quantile(0.75)
    avance_total = pd.cut(df_avance['Total'], bins=[float('-inf'), q1_avance, q2_avance, float('inf')],
                          labels=['Bajo', 'Medio', 'Alto']).values[-1]
    print("el avance es", avance_total)


    # Clasificar en categorías según cuartiles para avanceLecto
    df_avance_lecto = pd.DataFrame(lecto_dataset, columns=['Total'])
    q1_avance_lecto = df_avance_lecto['Total'].quantile(0.25)
    q2_avance_lecto = df_avance_lecto['Total'].median()
    q3_avance_lecto = df_avance_lecto['Total'].quantile(0.75)
    avance_total_lecto = pd.cut(df_avance_lecto['Total'], bins=[float('-inf'), q1_avance_lecto, q2_avance_lecto, float('inf')],
                          labels=['Bajo', 'Medio', 'Alto']).values[-1]
    
    print("el avance de la lecto essss:", avance_total_lecto)

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
        'avanceLectoescritura':avance_total_lecto,
        **temas_trabajados
    }

    return datos_transformados


