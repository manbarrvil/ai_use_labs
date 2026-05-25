# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 13:16:49 2025

@author: manba
"""

import os
import shutil as sh

directorio = r"C:/workspace/AI_USE_labs/AI_Manuel/data_set/"   # Ajusta si es necesario
dias = 364
minutos = 1443

for i in range(2, dias + 2):  # day_2 hasta day_365
    # Crear carpeta del día
    ruta_dia = os.path.join(directorio, f"day_{i}")
    os.makedirs(ruta_dia, exist_ok=True)

    # Crear carpetas minuto
    for j in range(3, minutos, 5):
        ruta_minuto = os.path.join(ruta_dia, f"minuto{str(j).zfill(4)}")
        os.makedirs(ruta_minuto, exist_ok=True)

print("Carpetas creadas correctamente")