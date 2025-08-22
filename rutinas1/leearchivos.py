from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql
from ruta_archivo import obtener_ruta_archivo
from agrega_registros import agregar_registros
from lee_no_ident import leelogforms
from lee_lista_sharepoint import imagenes_list
from lee_no_ident import leelogforms
from leeExcel import xls_a_df, xlsnew_a_df
from lee_ava import xlsava_a_df,crear_dataframe_desde_excel
import openpyxl
from openpyxl import load_workbook
import os
import time
import shutil
from pathlib import Path
import pandas as pd

import globales 

def leerarchivos():
    # ruta_carpeta = "C:\\planillas"
    ruta_carpeta = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\procesar"
    #ruta_carpeta = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\procesar_tester"   # para testeo

    ruta_destino = "C:\\procesados"
    #ruta_destino = "C:\\procesadostest"   # para testeo


    if 1==1 :
        cuentaArch = 0
        for archivo in os.listdir(ruta_carpeta):
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            nombre_archivo, extension = os.path.splitext(archivo)
            print(extension)
            resultado = inserta_archivo(ruta_archivo)
            id_archivo = resultado[1]
            try:
                ava=0
                if extension == '.txt':
                    df = txt_a_df(ruta_archivo, globales.globalperiodo, str(id_archivo))
                elif extension == '.xlsx' or extension == '.xlsm':
                    df_temp = pd.read_excel(ruta_archivo, nrows=1, usecols="A:B")

                    # Verificar si la celda A1 contiene "Nombre de usuario"
                    if df_temp.columns[0] == "Nombre de usuario":
                        ava = 1
                    elif df_temp.columns[0] == "newplanilla":    
                        df = xlsnew_a_df(ruta_archivo, str(id_archivo)) 
                    elif   df_temp.columns[1] == "course_name":
                        df= crear_dataframe_desde_excel(ruta_archivo, str(id_archivo)) 
                    else:
                        df = xls_a_df(ruta_archivo, globales.globalperiodo , str(id_archivo))
                
                if extension == '.xls' or ava==1:  
                    ava = 1 
                    df = xlsava_a_df(ruta_archivo, globales.globalperiodo , str(id_archivo))

                i = 1
                while os.path.exists(os.path.join(ruta_destino, f"{nombre_archivo}{extension}")):
                    nombre_archivo=f"{nombre_archivo}_{i}"
                    i += 1
                nuevo_nombre = f"{nombre_archivo}{extension}"
                ruta_destino_final = os.path.join(ruta_destino, nuevo_nombre)
              
                #workbook =  openpyxl.load_workbook("C:\\sudcraultra\\templates\\limpia.xlsx")
                
                #workbook.close()
                shutil.move(ruta_archivo, ruta_destino_final)
                
                cuentaArch += 1
                if ava == 1:
                    tabla = "lectura_avatemp"
                    #df.to_excel('verifica.xlsx', index=False) 
                    #nombre_archivo_txt = 'mi_dataframe.txt'
                    #df.to_csv(nombre_archivo_txt, sep='\t', index=False)
                    agregar_registros(df,tabla,[])
                else:
                    tabla = "lectura_temp"
                    agregar_registros(df,tabla,[])
                print("Archivo movidos exitosamente")
            except Exception as e:
                print(f"Archivo no leido: {nombre_archivo}")

                
            
            
            
            
           
            
            # Leer el archivo (código específico para leer el archivo)
            #ruta_archivo.rename(ruta_destino_final)
            
           
    #print("inicia datos de list shatrepoint")
    #sql="select max(id_lista) from imagenes; "
    #df=ejecutasql(sql)
    #print(df)

    #ultimo_leido = int(df.loc[0, 'max'])
    #imagenes_list(ultimo_leido)

    df=leelogforms()

    agregar_registros(df,'errores',[])
    
    path_base='C:/sudcraultra/Consultas/'
    
    mensaje=ejecutasqlarch(path_base + 'inserta_ava.sql')
    print(mensaje + '  -  Inserta datos de AVA')

    mensaje=ejecutasqlarch(path_base + 'borra_reprocesos.sql')
    print(mensaje + '  -  borra reprocesos')

   
    sql = 'SELECT * FROM matricula_eval_aux' 
    dfMat=ejecutasql(sql) #
    nombre_hoja='matricula_eval'
    agregar_registros(dfMat,nombre_hoja,[])
    
    #mensaje=ejecutasqlarch(path_base + 'inserta_no repetidos_eval_matriculados.sql')
    #print(mensaje + '  -  inserta eval_matricula')

    mensaje=ejecutasqlarch(path_base + 'inserta_no repetidos item_user.sql')
    print(mensaje + '  -  inserta item_user')

    #sql = 'SELECT * FROM matricula_eval_itemresp_aux2' 
    #dfMatI=ejecutasql(sql) #
    #nombre_hoja='matricula_eval_itemresp2'
    #agregar_registros(dfMatI,nombre_hoja,[])
   
    mensaje=ejecutasqlarch(path_base + 'inserta_resultados.sql')
    print(mensaje + '  -  inserta calificaciones obtenidas')

    mensaje=ejecutasqlarch(path_base + 'actualiza_nota.sql')
    print(mensaje + '  -  actualiza calificacion')

    mensaje=ejecutasqlarch(path_base + 'inserta_errores.sql')
    print(mensaje + '  -  inserta errores')

    mensaje=ejecutasqlarch(path_base + 'inserta_lectura.sql')
    print(mensaje + '  -  pasa lectura temp a lectura')

    mensaje=ejecutasqlarch(path_base + 'elimina_lecturatemp.sql')
    print(mensaje + '  -  elimina lectura temp')

    mensaje=ejecutasqlarch(path_base + 'actualiza_errores.sql')
    print(mensaje + '  -  actualiza errores')

    mensaje=ejecutasqlarch(path_base + 'actualiza_errores_inscripcion.sql')
    print(mensaje + '  -  actualiza errores inscripcion')   

    mensaje=ejecutasqlarch(path_base + 'actualiza_errores_eval.sql')
    print(mensaje + '  -  actualiza errores eval')

    mensaje=ejecutasqlarch(path_base + 'actualiza_errores_forma.sql')
    print(mensaje + '  -  actualiza errores eval forma')   

    mensaje=ejecutasqlarch(path_base + 'actualiza_errores_cierre.sql')
    print(mensaje + '  -  actualiza errores eval cierre') 

    mensaje=ejecutasqlarch(path_base + 'gestor_itemresp.sql')
    print(mensaje + '  -  gestión de tablas itemresp')  

    

    print("inicia lectura de logs imagenes")
    df=leelogforms()
    print(df)
    agregar_registros(df,'errores',[])

if __name__ == "__main__":
    leerarchivos()