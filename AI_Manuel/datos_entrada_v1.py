import pandas as pd
import numpy as np
#directorio = '/OPF_TFM/'
directorio = 'C:/workspace/AI/data_set/'
nudos_red = 14
rutasalida = 'C:/workspace/AI/inDATA/'
dias = 365
minutos = 1443

for dia in range(dias):
    for min in range(3, minutos, 5):
        # Guarda la potencia activa y reactiva de H_DATA en submatrizH
        with open(directorio+'day_'+str(dia+1)+'/minuto'+str(min).zfill(4)+'/LOAD_H_DATA.txt', 'r') as archivo:
            lineas = archivo.readlines()
            matriz = []
        for linea in lineas:
            fila = linea.strip().split(', ')  # Crea lista de cada línea eliminando espacios y comas
            matriz.append(fila)  # Agrega la lista de elementos a la matriz
        filas_matrizH = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        columnas_matrizH = [1, 2]
        submatrizH = [[float(matriz[i][j]) for j in columnas_matrizH] for i in filas_matrizH]

        # Crea la matriz_dataH con 14 filas(nudos), insertando ceros en los nudos donde no había consumo H
        matriz_dataH = []
        Nudos = [1, 3, 4, 5, 6, 8, 10, 11, 12, 14]
        aux = 0
        for i in range(nudos_red):
            if Nudos[aux] == i + 1:
                matriz_dataH.append([i + 1, submatrizH[aux][0], submatrizH[aux][1]])
                aux += 1
            else:
                matriz_dataH.append([i + 1, 0, 0])

        #  Crea la matriz_dataI con 14 filas(nudos), insertando ceros en los nudos donde no había consumo I
        with open(directorio+'day_'+str(dia+1)+'/minuto'+str(min).zfill(4)+'/LOAD_I_DATA.txt', 'r') as archivo:
            lineas = archivo.readlines()
        matriz = []
        for linea in lineas:
            fila = linea.strip().split(', ')
            matriz.append(fila)
        filas_matrizI = [1, 2, 3, 4, 5, 6, 7, 8]
        columnas_matrizI = [1, 2]
        submatrizI = [[float(matriz[i][j]) for j in columnas_matrizI] for i in filas_matrizI]

        matriz_dataI = []
        Nudos = [1, 3, 7, 9, 10, 12, 13, 14]
        aux = 0
        for i in range(nudos_red):
            if Nudos[aux] == i + 1:
                matriz_dataI.append([i + 1, submatrizI[aux][0], submatrizI[aux][1]])
                aux += 1
            else:
                matriz_dataI.append([i + 1, 0, 0])

        # Se crea matriz demanda 14x2. Consumos P y Q en cada nudo
        matriz_dataH = np.array(matriz_dataH)
        matriz_dataI = np.array(matriz_dataI)
        demanda = matriz_dataH[:, 1:3] + matriz_dataI[:, 1:3]

        # Guarda la P de generacion en submatrizG
        with open(directorio+'day_'+str(dia+1)+'/minuto'+str(min).zfill(4)+'/GEN_DATA.txt', 'r') as archivo:
            lineas = archivo.readlines()
        matriz = []
        for linea in lineas:
            fila = linea.strip().split(', ')
            matriz.append(fila)
        filas_matrizG = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        columnas_matrizG = [2]
        submatrizG = [[float(matriz[i][j]) for j in columnas_matrizG] for i in filas_matrizG]

        # Se crea matriz_dataG en la que se unen los nudos donde hay varias P generadas
        matriz_dataG = []
        Nudos = [3, 4, 5, 5, 5, 6, 7, 8, 9, 9, 9, 10, 10, 10, 11]
        i = 0
        while i < len(Nudos):
            if Nudos[i] in [5, 9, 10]:
                matriz_dataG.append([Nudos[i], submatrizG[i][0] + submatrizG[i + 1][0] + submatrizG[i + 2][0]])
                i += 3
            else:
                matriz_dataG.append([Nudos[i], submatrizG[i][0]])
                i += 1

        # Generacion con todos los nudos de la red
        generacion = []
        aux = 0
        for i in range(nudos_red):
            if aux < 9 and matriz_dataG[aux][0] == i + 1:
                generacion.append([i + 1, matriz_dataG[aux][1]])
                aux += 1
            else:
                generacion.append([i + 1, 0])

        # A la matriz demanda se le resta la generacion en la columna de P
        generacion = np.array(generacion)
        generacion = generacion[:, 1]
        demanda[:, 0] -= generacion

        # Se almacenan los valores de la matriz en una matriz 1x28 para crear el DataFrame
        valores = []
        for filas in demanda:
            for j in filas:
                valores.append(j)

        valores = np.array(valores)
        valoresT = valores.reshape(1, 28)

        # Creacion del DataFrame
        dato_minuto = pd.DataFrame(valoresT,
                               columns=['P1', 'Q1', 'P2', 'Q2', 'P3', 'Q3', 'P4', 'Q4', 'P5', 'Q5', 'P6', 'Q6', 'P7',
                                        'Q7', 'P8', 'Q8', 'P9', 'Q9', 'P10', 'Q10', 'P11', 'Q11', 'P12', 'Q12', 'P13',
                                        'Q13', 'P14', 'Q14'], index=['day'+str(dia+1)+'_min'+str(min).zfill(4)])

        if dia == 0 and min == 3:
            in_data = dato_minuto
        else:
            in_data = pd.concat([in_data, dato_minuto])


in_data.to_csv(rutasalida + 'prueba.txt')
