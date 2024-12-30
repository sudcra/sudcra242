import pandas as pd
from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql, hace_conexion , cierra_conexion
from datetime import date

df= ejecutasql("select * from convalidacion_dara")
# Supongamos que tu DataFrame se llama df y tiene las columnas 'archivo' y 'linea'
today = date.today()
date = today.strftime("%d-%m")
path_base='C:/sudcraultra/DARA/'
for index, row in df.iterrows():
    ruta_archivo = f"C:/sudcraultra/DARA/" + row['nombre_dara'] + "_" + date +".txt"
    with open(ruta_archivo, 'a') as m:
        logro = round(row['logro_obtenido']*100)
        if logro < 70:
            logro=70
        linea=row['nombre_dara'].ljust(23) + str(row['cod_plan']).ljust(7)+ str(row['cod_norma']).ljust(7)+ str(row['rut']).ljust(9).upper()+str(logro).ljust(4)+ '1'
        m.write(linea+ '\n')  
        