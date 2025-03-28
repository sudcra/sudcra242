from eval_insert import inserta_eval , crea_df_item_respuesta, hace_conexion , cierra_conexion
from ruta_archivo import obtener_ruta_archivo
from xlsx_a_df import convertir_a_df_tipo_0 , convertir_a_df_tipo_1
from agrega_registros import agregar_registros

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


"""
nombre_hoja="jjpp_sede"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="jjpp_programa"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
print(df)
agregar_registros(df,nombre_hoja,[])
"""