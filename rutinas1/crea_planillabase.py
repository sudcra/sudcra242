from eval_insert import  ejecutasql
import openpyxl
import xlwings as xw
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import quote_sheetname
from openpyxl.utils.dataframe import dataframe_to_rows
import shutil
import os


    

def Planillabase(cod_asig, prueba):
    path_base='C:/sudcraultra/Consultas/'
    archivo = open(path_base + 'consulta_eval.sql', "r")
    sql= archivo.read()
    sql = sql.replace("[cod_asig]", cod_asig)
    sql = sql.replace("[num_prueba]", str(prueba))
    dfa=ejecutasql(sql)
    
    archivo = open(path_base + 'consulta_item.sql', "r")
    sql= archivo.read()
    sql = sql.replace("[cod_asig]", cod_asig)
    sql = sql.replace("[num_prueba]",str(prueba))
    dfi=ejecutasql(sql)

    archivo = open(path_base + 'consulta_escala.sql', "r")
    sql= archivo.read()
    sql = sql.replace("[cod_asig]", cod_asig)
    sql = sql.replace("[num_prueba]", str(prueba))
    dfe=ejecutasql(sql)

    copiar_datos_a_excel(dfa, dfi, dfe)



def copiar_datos_a_excel(dfa, dfi, dfe, ruta_excel=r'C:\sudcraultra_access\SISTEMA\MODELO_NEW.xlsm'):
    # Obtener el nombre del archivo a partir del valor de la columna 0 de dfa
    nuevo_nombre = f"{dfa.iloc[0, 0]}.xlsm"
    
    # Hacer una copia del archivo original
    ruta_destino = rf'C:\sudcraultra_access\SISTEMA\planillas_base\{nuevo_nombre}'
    shutil.copy(ruta_excel, ruta_destino)
    
    # Abrir el libro Excel copiado con xlwings
    app = xw.App(visible=False)
    libro = app.books.open(ruta_destino)
    
    # Crear un diccionario con los DataFrames y sus respectivas hojas destino
    hojas_datos = {
        'Eval': dfa,
        'item': dfi,
        'escala': dfe
    }
    
    # Iterar sobre cada hoja y su correspondiente DataFrame
    for hoja_nombre, df in hojas_datos.items():
        try:
            hoja = libro.sheets[hoja_nombre]
            
            # Desproteger la hoja para poder editar
            hoja.api.Unprotect(Password='arcdus')
            
            # Limpiar el contenido actual de la hoja, excepto la primera fila
            hoja.range('A2').options(expand='table').clear_contents()
            
            # Insertar los datos del DataFrame en la hoja a partir de la fila 2 (sin encabezados)
            hoja.range('A2').value = df.values
            
            # Proteger la hoja después de editar
            #hoja.api.Protect(Password='arcdus')
        except KeyError:
            print(f"La hoja '{hoja_nombre}' no existe en el archivo Excel.")
    
    # Ocultar columnas de la hoja 'SECCION' de la columna 6 a la 35 si la fila 6 está vacía
    try:
        hoja_seccion = libro.sheets['SECCION']
        #hoja_seccion.api.Unprotect(Password='arcdus')
        for col in range(6, 36):
            if hoja_seccion.cells(6, col).value is None:
                hoja_seccion.range((1, col)).api.EntireColumn.Hidden = True
        
        # Ocultar la columna D si el valor en la columna 6 de dfa es False
        if dfa.iloc[0, 6] == False:
            hoja_seccion.range('D:D').api.EntireColumn.Hidden = True
        
        # Ocultar la columna E si el valor en la columna 11 de dfa es False
        if dfa.iloc[0, 10] == False:
            hoja_seccion.range('E:E').api.EntireColumn.Hidden = True
        
        # Proteger la hoja después de editar
        #hoja_seccion.api.Protect(Password='arcdus')
    except KeyError:
        print("La hoja 'SECCION' no existe en el archivo Excel.")
    
    # Guardar y cerrar el libro Excel
    libro.save()
    libro.close()
    app.quit()
    print(f"Datos copiados correctamente en el archivo {ruta_destino}.")

# Uso del ejemplo
# copiar_datos_a_excel(dfa, dfi, dfe)


    
if __name__ == "__main__":
    
    Planillabase('MAT4111',11)
    Planillabase('MAT4140',11)
    Planillabase('MAT4141',11)
    Planillabase('MAT4160',11)
    Planillabase('MAT5130',2)
    



    


