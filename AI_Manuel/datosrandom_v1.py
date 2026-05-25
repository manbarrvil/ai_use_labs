import numpy as np

media = 0
desviacion_estandar = 1
desviacion_estandar_gen = 1
carpetasminutos = 1443
directorio = r"C:/workspace/AI_USE_labs/AI_Manuel/data_set/"

#for dia in range(5):
for dia in range(364):
    for min in range(3, carpetasminutos, 5):

        # Lee los datos
        with open(directorio+'day_1/minuto' + str(min).zfill(4) + '/LOAD_H_DATA.txt', 'r') as archivo:
            lineas = archivo.readlines()
        matriz = []
        for linea in lineas:
            fila = linea.strip().split(', ')  # Crea lista de cada línea eliminando espacios y comas
            matriz.append(fila)  # Agrega la lista de elementos a la matriz
        filas_matrizH = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        columnas_matrizH = [1, 2]
        submatrizH = [[float(matriz[i][j]) for j in columnas_matrizH] for i in filas_matrizH]

        # Potencia máxima de los nudos con consumo residencial
        P_H = [15., 0.276, 0.432, 0.725, 0.55, 0.588, 0.477, 0.331, 15., 0.207]
        Q_H = [3.1, 0.069, 0.108, 0.182, 0.138, 0.147, 0.12, 0.083, 3., 0.052]

        # Escribe el nuevo archivo
        new_matrizH = []
        Nudos = [1, 3, 4, 5, 6, 8, 10, 11, 12, 14]
        fila1 = ['Nudo', '   P', '   Q']
        new_matrizH.append(fila1)
        for i in range(10):
            numrandom = round(np.random.normal(loc=media, scale=desviacion_estandar),4) # Crea numero aleatorio
            x_PH = numrandom * P_H[i]
            x_QH = numrandom * Q_H[i]
            modPH = float(format(x_PH, ".8f")) #round(numrandom * P_H[i], 4)
            modQH = float(format(x_QH, ".8f"))

            # Si el nuevo valor al sumarle la potencia es negativo lo sustituye por cero
            if submatrizH[i][0] + modPH < 0:
                submatrizH[i][0] = 0
            else:
                    submatrizH[i][0] += modPH
            if submatrizH[i][1] + modQH < 0:
                submatrizH[i][1] = 0
            else:
                    submatrizH[i][1] += modQH

            new_matrizH.append([Nudos[i], round(submatrizH[i][0], 8), round(submatrizH[i][1], 8)])


        with open(directorio+'day_' + str(dia+2) + '/minuto' + str(min).zfill(4) + '/LOAD_H_DATA.txt', 'w') as archivo:
            for fila in new_matrizH:
                linea = ', '.join(map(str, fila))
                archivo.write(linea + '\n')



# Lee LOAD_I_DATA
        with open(directorio + 'day_1/minuto' + str(min).zfill(4) + '/LOAD_I_DATA.txt', 'r') as archivo:
            lineas = archivo.readlines()
        matriz = []
        for linea in lineas:
            fila = linea.strip().split(', ')
            matriz.append(fila)
        filas_matrizI = [1, 2, 3, 4, 5, 6, 7, 8]
        columnas_matrizI = [1, 2]
        submatrizI = [[float(matriz[i][j]) for j in columnas_matrizI] for i in filas_matrizI]

        # Potencia máxima de los nudos con consumo industrial
        P_I = [5., 0.224, 0.077, 0.574, 0.068, 5., 0.032, 0.33]
        Q_I = [1., 0.139, 0.048, 0.356, 0.042, 1.7, 0.02, 0.205]

        # Escribe el nuevo archivo
        new_matrizI = []
        Nudos = [1, 3, 7, 9, 10, 12, 13, 14]
        fila1 = ['Nudo', '   P', '   Q']
        new_matrizI.append(fila1)
        for i in range(8):
            numrandom = round(np.random.normal(loc=media, scale=desviacion_estandar),4)  # Crea numero aleatorio
            modPI = round(numrandom * P_I[i],4)
            modQI = round(numrandom * Q_I[i],4)

            # Si el nuevo valor al sumarle la potencia es negativo lo sustituye por cero
            if submatrizI[i][0] + modPI < 0:
                submatrizI[i][0] = 0
            else:
                submatrizI[i][0] += modPI
            if submatrizI[i][1] + modQI < 0:
                submatrizI[i][1] = 0
            else:
                submatrizI[i][1] += modQI

            new_matrizI.append([Nudos[i], round(submatrizI[i][0], 8), round(submatrizI[i][1], 8)])

        with open(directorio+'day_' + str(dia+2) + '/minuto' + str(min).zfill(4) + '/LOAD_I_DATA.txt', 'w') as archivo:
            for fila in new_matrizI:
                linea = ', '.join(map(str, fila))
                archivo.write(linea + '\n')


# Lee datos generación
        with open(directorio+'day_1/minuto' + str(min).zfill(4) + '/GEN_DATA.txt', 'r') as archivo:
            lineas = archivo.readlines()
        matriz = []
        for linea in lineas:
            fila = linea.strip().split(', ')
            matriz.append(fila)
        filas_matrizG = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        columnas_matrizG = [2]
        submatrizG = [[float(matriz[i][j]) for j in columnas_matrizG] for i in filas_matrizG]

        # Potencia máxima de los nudos con generación
        P_G = [0.02, 0.02, 0.03, 0.6, 0.033, 0.03, 1.5, 0.03, 0.03, 0.310, 0.212, 0.04, 0.2, 0.014, 0.01]


        # Escribe el nuevo archivo GEN
        new_matrizG = []
        Nombre = ['GP3', 'GP4', 'GP5', 'GB5', 'GFC5', 'GP6', 'GWT7', 'GP8', 'GP9', 'GCHPD9', 'GCHPFC9', 'GP10', 'GB10', 'GFC10', 'GP11']
        Nudos = [3, 4, 5, 5, 5, 6, 7, 8, 9, 9, 9, 10, 10, 10, 11]
        Pmax = [0.02, 0.02, 0.03, 0.5, 0.033, 0.03, 1.5, 0.03, 0.03, 0.31, 0.212, 0.04, 0.2, 0.014, 0.01]
        Pmin = [0, 0, 0, -0.5, -0.033, 0, 0, 0, 0, 0, 0, 0, -0.2, -0.014, 0]
        fila1 = ['Nombre', 'Nudo', '   P', '   Pmax', 'Pmin']
        new_matrizG.append(fila1)
        for i in range(15):
            numrandom = abs(round(np.random.normal(loc=media, scale=desviacion_estandar_gen),4))  # Crea numero aleatorio
            modPG = round(numrandom * P_G[i],4)

            # Si el nuevo valor al sumarle la potencia es negativo lo sustituye por cero
            if submatrizG[i][0] + modPG < 0:
                submatrizG[i][0] = 0
            else:
                submatrizG[i][0] += modPG

            new_matrizG.append([Nombre[i], Nudos[i], round(submatrizG[i][0], 8), Pmax[i], Pmin[i]])

        with open(directorio+'day_' + str(dia + 2) + '/minuto' + str(min).zfill(4) + '/GEN_DATA.txt', 'w') as archivo:
            for fila in new_matrizG:
                linea = ', '.join(map(str, fila))
                archivo.write(linea + '\n')