import os
import shutil

import pandas as pd

def leelogforms():
    ruta_carpeta = "C:/Users/lgutierrez/OneDrive - Fundacion Instituto Profesional Duoc UC/SUDCRA/logforms"
    ruta_destino = "C:/procesados/logprocesados"
    df1 = pd.DataFrame(columns=['imagen'])
    for archivo in os.listdir(ruta_carpeta):
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        nombre_archivo, extension = os.path.splitext(archivo)
        with open(ruta_archivo, "r") as archivo:
            nombres_archivo = []
            etiquetas = []
            try:
                for i, linea in enumerate(archivo):
                    if i >= 26:  # Comenzar desde la línea 27
                        if not linea.strip():
                            break    
                        valores=linea.strip().split()
                        if len(valores)>=2 and valores[1]=='Sin':
                            nombre_imagen, etiqueta = valores[0], valores[1]
                            nombres_archivo.append(nombre_imagen)
                            etiquetas.append(etiqueta)
                        # Detener si se encuentra una línea en blanco
                        
                        # Agregar la línea a la lista
            except Exception as e:
                print(e)       
    
        df = pd.DataFrame({"imagen": nombres_archivo})
        frames = [df1, df]
        df1 = pd.concat(frames, ignore_index=True)    
        #print(df)

       
        

        i = 1
        while os.path.exists(os.path.join(ruta_destino, f"{nombre_archivo}{extension}")):
            nombre_archivo=f"{nombre_archivo}_{i}"
            i += 1
        
        nuevo_nombre = f"{nombre_archivo}{extension}"
        ruta_destino_final = os.path.join(ruta_destino, nuevo_nombre)
        
        # Leer el archivo (código específico para leer el archivo)
        
        shutil.move(ruta_archivo, ruta_destino_final)
    return df1

