from eval_insert import inserta_eval , crea_df_item_respuesta, hace_conexion , cierra_conexion
from ruta_archivo import obtener_ruta_archivo
from xlsx_a_df import convertir_a_df_tipo_0 , convertir_a_df_tipo_1
from agrega_registros import agregar_registros

ruta = obtener_ruta_archivo('C:/')

nombre_hoja="matricula"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])

nombre_hoja="inscripcion"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])

"""
nombre_hoja="convalidacion"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="asignaturas"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
print(df)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="alumnos"
df = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(df,nombre_hoja,[])

nombre_hoja="docentes"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])

nombre_hoja="planes"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])

nombre_hoja="sedes"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])

nombre_hoja="matricula"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])


nombre_hoja="secciones"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])

nombre_hoja="inscripcion"
dfim = convertir_a_df_tipo_0(ruta, nombre_hoja)
agregar_registros(dfim,nombre_hoja,[])
"""