import subprocess, os, time

dias = 366

minutos = 1443

directorio = 'C:/workspace/AI/data_set/day_1/'
os.chdir(directorio)                                 # Accedo a la carpeta donde se encuentra el modelo GAMS
# for dia in range(0, dias):                              # Ejecuta conv_data para crear todos los .g00
#     for min in range(3, minutos, 5):
#         comando = ('gams conv_data.gms s=C:\workspace\AI\data_set\day_'+str(dia+1)+'\minuto'+str(min).zfill(4)+
#                    ' Idir=C:\workspace\AI\data_set\day_'+str(dia+1)+'\minuto'+str(min).zfill(4))
#                    #' Idir=minuto'+str(min).zfill(4))

#         resultado = subprocess.run(comando, shell=True)
         # time.sleep(0.01)

for dia in range(0,dias):                            # Ejecuta MinPerd_PF para crear todos los .put
    for min in range(3, minutos, 5):
        comando = ('gams MinPerd_Base_perdidas_Qopt_v2.gms r=C:\workspace\AI\data_set\day_'+str(dia+1)+'\minuto'+str(min).zfill(4)+
                   ' Pdir=C:\workspace\AI\data_set\day_'+str(dia+1)+' --Num= min'+str(min).zfill(4))
                   #' --Num= min'+str(min).zfill(4))


        resultado = subprocess.run(comando, shell=True)
        time.sleep(0.02)
        print("Ejecutando:", comando)





 # Comando para ejecutar MinPerd_PF_MV.gms
 # comando = "gams MinPerd_PF_MV.gms  r=C:\OPF_TFM\day_2\minuto0003 Pdir=C:\OPF_result\day_2 --Num= min0003"

 # Comando para ejecutar conv_data.gms
 # comando = "gams conv_data.gms s=C:\OPF_TFM\day_2\minuto0003 Idir=C:\OPF_TFM\day_2\minuto0003"