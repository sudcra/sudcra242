from eval_insert import inserta_eval , crea_df_item_respuesta, hace_conexion , cierra_conexion
from ruta_archivo import obtener_ruta_archivo
from xlsx_a_df import convertir_a_df_tipo_0 , convertir_a_df_tipo_1
from agrega_registros import agregar_registros
import os

ruta = obtener_ruta_archivo('C:')

nombre_hoja="alumnos"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
#print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="asignaturas"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
#print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="docentes"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
#print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="matricula"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
#print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="secciones"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
#print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="inscripcion"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
#print(df)
agregar_registros(df,nombre_hoja,[])

# ----------------------------------------
# Actualización estudiantes de intercambio
# ----------------------------------------

# Obtener la ruta de la carpeta seleccionada
carpeta_ruta = os.path.dirname(ruta)

# Generar la ruta a "alumnos_intercambio.xlsx" 
ruta_fija1 = os.path.join(carpeta_ruta, "alumnos_intercambio.xlsx")

nombre_hoja = "alumnos"
df = convertir_a_df_tipo_0(ruta_fija1, nombre_hoja)
agregar_registros(df, nombre_hoja, [])

nombre_hoja = "matricula"
df = convertir_a_df_tipo_0(ruta_fija1, nombre_hoja)
agregar_registros(df, nombre_hoja, [])

nombre_hoja = "inscripcion"
df = convertir_a_df_tipo_0(ruta_fija1, nombre_hoja)
agregar_registros(df, nombre_hoja, [])


# ----------------------------------------
# Actualización estudiantes cambio sexo
# ----------------------------------------

# Obtener la ruta de la carpeta seleccionada
carpeta_ruta = os.path.dirname(ruta)

# Generar la ruta a "alumnos_intercambio.xlsx" 
ruta_fija2 = os.path.join(carpeta_ruta, "alumnos_cambio_sexo.xlsx")

nombre_hoja = "alumnos"
df = convertir_a_df_tipo_0(ruta_fija2, nombre_hoja)
agregar_registros(df, nombre_hoja, [])

# ----------------------------------------
"""nombre_hoja="jjpp_sede"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="jjpp_programa"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
print(df)
agregar_registros(df,nombre_hoja,[])
"""