import os
import pandas as pd
import xlsxwriter

def juntatxt():
    # Ruta de la carpeta donde se encuentran los archivos .txt
    ruta_carpeta = "c:/sudcraultra/lectura/procesados"

    # Nombre del archivo de salida
    nombre_archivo_salida = "reproceso.txt"

    # Abre el archivo de salida en modo escritura
    with open(nombre_archivo_salida, "w") as archivo_salida:
        # Recorre todos los archivos en la carpeta
        for nombre_archivo in os.listdir(ruta_carpeta):
            if nombre_archivo.endswith(".txt"):
                ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
                with open(ruta_completa, "r") as archivo_entrada:
                    # Lee cada línea del archivo
                    for linea in archivo_entrada:
                        # Si la línea comienza con "1", escríbela en el archivo de salida
                        if linea.strip().startswith("1"):
                            archivo_salida.write(linea)

    print(f"Se han almacenado las líneas que comienzan con '1' en el archivo '{nombre_archivo_salida}'.")

 

import pandas as pd
import xlsxwriter

# Crear un DataFrame de prueba
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Crear un archivo Excel con xlsxwriter
with pd.ExcelWriter('Formato_Condicional10.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='Hoja1', index=False)

    # Obtener el objeto workbook
    workbook = writer.book
    formatonum= '"NL"'
    formato_condicional1 = workbook.add_format({'num_format': formatonum})
    formatonum= '"PL"'
    formato_condicional2 = workbook.add_format({'num_format': formatonum})
    formatonum= '"L"'
    formato_condicional3 = workbook.add_format({'num_format': formatonum})
    rango = 'A2:B12'
    writer.sheets['Hoja1'].conditional_format(rango, {'type': 'cell', 'criteria': '=', 'value': 1, 'format': formato_condicional1})
    writer.sheets['Hoja1'].conditional_format(rango, {'type': 'cell', 'criteria': '=', 'value': 2, 'format': formato_condicional2})
    writer.sheets['Hoja1'].conditional_format(rango, {'type': 'cell', 'criteria': '=', 'value': 3, 'format': formato_condicional3})

print("Archivo 'Formato_Condicional2.xlsx' creado con formato condicional.")