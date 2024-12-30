import pandas as pd
from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql, hace_conexion , cierra_conexion

df= ejecutasql("select * from para_txt")
# Supongamos que tu DataFrame se llama df y tiene las columnas 'archivo' y 'linea'

path_base='C:/sudcraultra/lectura/procesados/'
with open(f'C:/sudcraultra/lectura/procesar/reproceso_26-03.txt', 'w') as m:
    for index, row in df.iterrows():
        archivo = path_base + row['archivo']
        linea = int(row['linea_leida'])
        
        # Leer el archivo
        with open(archivo, 'r') as f:
            lines = f.readlines()
            if linea <= len(lines):
                m.write(lines[linea])  
        # Obtener la línea específica (indexado desde 0)
            else:
                print(f"La línea {linea} está fuera del rango del archivo {row['archivo']}")
  
    
  
 