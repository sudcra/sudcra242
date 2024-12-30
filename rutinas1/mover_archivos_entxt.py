# Este script realiza lo siguiente:
# 1. Abre una ventana de explorador de archivos para seleccionar un archivo de texto que contiene una lista de nombres de archivo (con extensión).
# 2. Crea un DataFrame a partir de los nombres de archivo obtenidos del archivo de texto.
# 3. Define dos rutas: una carpeta de origen donde se buscarán los archivos y otra carpeta de destino donde se moverán.
# 4. Mueve los archivos listados desde la carpeta de origen a la carpeta de destino.

import pandas as pd
import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Paso 1: Abrir una ventana de explorador de archivos para seleccionar el archivo de texto
Tk().withdraw()  # Oculta la ventana principal de Tk
archivo_lista = askopenfilename(title="Seleccionar archivo de texto con la lista de nombres de archivo", 
                                filetypes=[("Archivos de texto", "*.txt")])

if not archivo_lista:
    print("No se seleccionó ningún archivo. Saliendo del programa.")
    exit()

# Paso 2: Leer el archivo de texto y cargar los nombres en un DataFrame
try:
    with open(archivo_lista, "r") as file:
        nombres_archivos = [line.strip() for line in file.readlines()]
    
    # Crear un DataFrame con la lista de nombres de archivo
    df = pd.DataFrame(nombres_archivos, columns=["NombresArchivos"])
    print("DataFrame creado con los siguientes datos:")
    print(df)
except Exception as e:
    print(f"Error al leer el archivo de texto: {e}")
    exit()

# Paso 3: Definir las rutas de origen y destino
ruta_origen = r"C:\\procesados"
ruta_destino = r"C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\procesar"

# Validar que las rutas existen
if not os.path.exists(ruta_origen):
    print(f"La ruta de origen no existe: {ruta_origen}")
    exit()

if not os.path.exists(ruta_destino):
    print(f"La ruta de destino no existe: {ruta_destino}")
    exit()

# Paso 4: Mover los archivos
for nombre_archivo in df["NombresArchivos"]:
    origen = os.path.join(ruta_origen, nombre_archivo)
    destino = os.path.join(ruta_destino, nombre_archivo)

    try:
        if os.path.exists(origen):
            shutil.move(origen, destino)
            print(f"Archivo movido: {nombre_archivo}")
        else:
            print(f"El archivo no existe en la carpeta de origen: {nombre_archivo}")
    except Exception as e:
        print(f"Error al mover el archivo {nombre_archivo}: {e}")

print("Proceso completado.")
