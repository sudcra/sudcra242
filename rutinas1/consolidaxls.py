import pandas as pd
import os
columnsdf=["alumno_rut" , "nombre_alumno" , "id_curso" , "tipo_item" , "nombre_item" , "fecha_ult_acceso_item" , "min_ult_acceso_item" , "realizo_actividad" , "score" , "possible_score" , "fecha_ult_envio" , "progreso_accesos" , "progreso_envios" , "fecha_extraccion"]
#columnsbd=["ANO","SEMESTRE","SEDE","INSTITUCION","SALIDA INTERMEDIA","VERIFICACION SI","CODCARRERA","NOMCARRERA","MODALIDAD","JORNADA","RUT","NOMBRES","APPATERNO","APMATERNO","SEXO","FNAC","ESTADO CIVIL","NACIONALIDAD","TIPO INGRESO","MOL","SUBTIPO","ANO INGRESO","SEM INGRESO","FECHMATR","CONDICION","USERNAME","NOMBRE COLEGIO","TIPO COLEGIO","TIPO ESTUDIO","PROMEDIO LEM","EGRESO EM","ANO PSU","PROM PSU"]


#columnsdf=["ANO","SEMESTRE","SEDE"]

# Abre la hoja de Excel
# Obtener la lista de archivos en el directorio
files = os.listdir("C:/SUDCRApy/datosSAP/indice")
df2 = pd.DataFrame()
# Filtrar los archivos Excel
excel_files = [file for file in files if file.endswith(".csv")]

# Recorrer los archivos Excel
for file in excel_files:
    pathfile= "C:/SUDCRApy/datosSAP/indice/" + file
    print(pathfile)
    df = pd.read_csv(pathfile, sep=';')
    df2 = pd.concat([df2,df])

"""df2.rename(columns={'AÑO': 'ANO'}, inplace=True)
df2.rename(columns={'AÑO INGRESO': 'ANO INGRESO'}, inplace=True)
df2.rename(columns={'AÑO PSU': 'ANO PSU'}, inplace=True)"""

df2=df2[columnsdf]

df2.to_csv('C:/SUDCRApy/datosSAP/detalle.csv', index=False, sep=";", encoding='utf-8-sig')


 #df = pd.read_excel("my_sheet.xlsx", skiprows=1)
# Crea una conexión a la base de datos de Access
