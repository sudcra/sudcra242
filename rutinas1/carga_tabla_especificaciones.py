from eval_insert import inserta_eval , crea_df_item_respuesta, hace_conexion , cierra_conexion
from ruta_archivo import obtener_ruta_archivo
from xlsx_a_df import convertir_a_df_tipo_0 , convertir_a_df_tipo_1
from agrega_registros import agregar_registros
import os
import tkinter as tk
from tkinter import filedialog

def cargaTablaEspecificaciones(ruta):
    ava = 0

    respuesta=inserta_eval(ruta)

    if respuesta[2] == 'Registro insertado correctamente' or ava == 1:
        cod_asig = respuesta[0]
        prueba = respuesta[1]
        nombre_hoja="medidas"
        df = convertir_a_df_tipo_0(ruta, nombre_hoja)

        agregar_registros(df,nombre_hoja,[])

        nombre_hoja="escala"
        df = convertir_a_df_tipo_0(ruta, nombre_hoja) 

        agregar_registros(df,nombre_hoja,[])


        nombre_hoja="calificaciones"
        df = convertir_a_df_tipo_0(ruta, nombre_hoja)

        agregar_registros(df,nombre_hoja,[])

        nombre_hoja="item"
        df = convertir_a_df_tipo_0(ruta, nombre_hoja)
        dfi = df.iloc[:, :-4]
        agregar_registros(dfi,nombre_hoja,[])

        nombre_hoja="item_medida"
        dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)

        agregar_registros(dfim,nombre_hoja,[])

        nombre_hoja="item_respuesta"
        dfire=crea_df_item_respuesta(df, cod_asig, prueba)
        #print(dfire)
        agregar_registros(dfire,nombre_hoja,[])
    else:
        print("La tabla ya fue cargada con anterioridad.")

def obtener_rutas_xlsm(carpeta):
    rutas_xlsm = []
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            if file.endswith('.xlsm'):
                rutas_xlsm.append(os.path.join(root, file))
    return rutas_xlsm

def elegir_carpeta():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    carpeta = filedialog.askdirectory()  # Abre el cuadro de diálogo para elegir carpeta
    if carpeta:
       return carpeta
    else:
        print("No se seleccionó ninguna carpeta")
        return ""
    
if __name__ == "__main__":         

    tablas = obtener_rutas_xlsm(elegir_carpeta())  

    for tabla in tablas:
        cargaTablaEspecificaciones(tabla)
    #ruta = obtener_ruta_archivo("C:/sudcraultra_access/Etica_ok/")
   # cargaTablaEspecificaciones(ruta)