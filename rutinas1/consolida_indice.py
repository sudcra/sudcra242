

#Consolida los XLS descagados de SAP en un único archivo .csv
import pandas as pd
import os
columnsdf=["ANO","SEMESTRE","SEDE","INSTITUCION","SALIDA INTERMEDIA","VERIFICACION S.I.","COD.CARRERA","NOM.CARRERA","MODALIDAD","JORNADA","RUT","NOMBRES","AP.PATERNO","AP.MATERNO","SEXO","FNAC","ESTADO CIVIL","NACIONALIDAD","TIPO INGRESO","M.O.L","SUBTIPO","ANO INGRESO","SEM INGRESO","FE.CH.MATR","CONDICION","USERNAME","NOMBRE COLEGIO","TIPO COLEGIO","TIPO ESTUDIO","PROM.LEM","EGRESO EM","ANO PSU","PROM.PSU"]
#columnsbd=["ANO","SEMESTRE","SEDE","INSTITUCION","SALIDA INTERMEDIA","VERIFICACION SI","CODCARRERA","NOMCARRERA","MODALIDAD","JORNADA","RUT","NOMBRES","APPATERNO","APMATERNO","SEXO","FNAC","ESTADO CIVIL","NACIONALIDAD","TIPO INGRESO","MOL","SUBTIPO","ANO INGRESO","SEM INGRESO","FECHMATR","CONDICION","USERNAME","NOMBRE COLEGIO","TIPO COLEGIO","TIPO ESTUDIO","PROMEDIO LEM","EGRESO EM","ANO PSU","PROM PSU"]


#columnsdf=["ANO","SEMESTRE","SEDE"]

# Abre la hoja de Excel
# Obtener la lista de archivos en el directorio
files = os.listdir("C:\\sudcraultra_access\\datos_sap\\indice")
df2 = pd.DataFrame()
# Filtrar los archivos Excel
excel_files = [file for file in files if file.endswith(".XLS")]

# Recorrer los archivos Excel
for file in excel_files:
    pathfile= "C:\\sudcraultra_access\\datos_sap\\indice\\" + file
    print(pathfile)
    df = pd.read_excel(pathfile, skiprows=1)   
    df2 = pd.concat([df2,df])

df2.rename(columns={'AÑO': 'ANO'}, inplace=True)
df2.rename(columns={'AÑO INGRESO': 'ANO INGRESO'}, inplace=True)
df2.rename(columns={'AÑO PSU': 'ANO PSU'}, inplace=True)

df2=df2[columnsdf]

df2.to_csv('C:\\sudcraultra_access\\datos_sap\\INDICE.csv', index=False, sep=";", encoding='utf-8-sig')


 #df = pd.read_excel("my_sheet.xlsx", skiprows=1)
# Crea una conexión a la base de datos de Access
