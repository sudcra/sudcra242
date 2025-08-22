from eval_insert import inserta_eval , crea_df_item_respuesta, hace_conexion , cierra_conexion
from xlsx_a_df import convertir_a_df_tipo_0 , convertir_a_df_tipo_1
from agrega_registros_252 import agregar_registros
from agrega_registros_252_alumno import cargar_alumnos
from agrega_registros_252_docente import cargar_docentes
from agrega_registros_252_seccion import cargar_secciones
from agrega_registros_252_matricula import sync_matricula
from agrega_registros_252_inscripcion import sync_inscripcion

def carga_tabla_actualiza(ruta):
    nombre_hoja="alumnos"
    df = convertir_a_df_tipo_0(ruta, nombre_hoja)
    # print(df)
    cargar_alumnos(df,nombre_hoja,[])

    nombre_hoja="asignaturas"
    df = convertir_a_df_tipo_0(ruta, nombre_hoja)
    # print(df)
    agregar_registros(df,nombre_hoja,[])

    nombre_hoja="docentes"
    df = convertir_a_df_tipo_0(ruta, nombre_hoja)
    # print(df)
    cargar_docentes(df,nombre_hoja,[])

    nombre_hoja="matricula"
    df = convertir_a_df_tipo_0(ruta, nombre_hoja)
    # print(df)
    sync_matricula(df,[])

    nombre_hoja="secciones"
    df = convertir_a_df_tipo_0(ruta, nombre_hoja)
    # print(df)
    cargar_secciones(df,nombre_hoja,[])

    nombre_hoja="inscripcion"
    df = convertir_a_df_tipo_0(ruta, nombre_hoja)
    # print(df)
    sync_inscripcion(df,[])

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
