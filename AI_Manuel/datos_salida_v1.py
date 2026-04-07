import pandas as pd
import numpy as np
directorio = 'C:/workspace/AI/data_set/'
nudos_red = 14
rutasalida = 'C:/workspace/AI/outDATA/'
dias = 365
minutos = 1443
Sb = 10 #MVA

for dia in range(dias):
    print('Dia:'+str(dia))
    for min in range(3, minutos, 5):
        # Lee el .txt y crea la lista lineas donde cada elemento es una linea del archivo
        with open(directorio+'day_'+str(dia+1)+'/RESULT_B2B_min'+str(min).zfill(4)+'.put', 'r') as archivo:
            lineas = archivo.readlines()

        # Creo una matriz donde guardo la linea de la 10 a la 23 donde están los datos de tensiones
        matriz = []
        for i in range(10, 24):
            linea = lineas[i]
            fila = linea.split('          ')  # Crea lista de cada línea eliminando espacios
            matriz.append(fila)
        for j in range(30, 43):
            linea = lineas[j]
            fila = linea.split('          ')  # Crea lista de cada línea eliminando espacios
            matriz.append(fila)
        # Añado perdidas
        fila = lineas[0].split(' ')
        matriz.append(fila)
        # Añado PQ slack
       # fila = lineas[43].split(' ')
       # matriz.append(fila)
       # fila = lineas[44].split(' ')
       # matriz.append(fila)

        # En matriz_V (15x1) guardo los datos de las tensiones pasándolos a flotantes
        #filas_matriz = range(len(matriz))
        filas_matriz = len(matriz)
        columnas_matriz = [1]
        #matriz_V = [[float(matriz[i][j]) for j in columnas_matriz] for i in filas_matriz]
        matriz_V = []
        for fila in matriz:
            if len(fila) > 1:
                try:
                    matriz_V.append(float(fila[1]))
                except:
                    matriz_V.append(np.nan)
            else:
                matriz_V.append(np.nan)

        matriz_V = np.array(matriz_V).reshape(1, len(matriz_V))

        # Paso matriz_V a (1x15) y creo el DataFrame
#        matriz_V = np.array(matriz_V)
#        matriz_V = matriz_V.reshape(1, len(matriz_V))
        dato_minuto = pd.DataFrame(matriz_V,
                                   columns=['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12',
                                            'V13', 'V14','I0_1','I0_12','I1_2','I2_3','I3_4','I4_5','I5_6','I7_8','I8_3','I8_9','I9_10','I10_11','I12_13', 'PERD'], index=['day'+str(dia+1)+'_min'+str(min).zfill(4)])

        if dia == 0 and min == 3:
            out_data = dato_minuto
        else:
            out_data = pd.concat([out_data, dato_minuto])

out_data.to_csv(rutasalida + 'outset.txt')

