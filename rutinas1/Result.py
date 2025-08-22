import os
import pandas as pd
from eval_insert import  hace_conexion , cierra_conexion

def generar_archivos_convalidados(ruta_base, conn):
    try:
        # Verificar si la carpeta 'convalidados' existe, si no, crearla
        ruta_convalidados = os.path.join(ruta_base, 'resultados')
        if not os.path.exists(ruta_convalidados):
            os.makedirs(ruta_convalidados)

        # Consulta SQL proporcionada
        consulta = """
        SELECT  
        sd.nombre_sede,
        asig.cod_asig,
        asig.asig,
        s.seccion,
        al.rut,
        al.nombres,
        al.apellidos,
        e.nombre_prueba,
        co.logro_obtenido,
        ca.condicion
        FROM calificaciones_obtenidas co
        JOIN calificaciones ca ON ca.id_calificacion = co.id_calificacion
        JOIN matricula_eval me ON me.id_matricula_eval = co.id_matricula_eval
        JOIN matricula mt ON mt.id_matricula = me.id_matricula 
        JOIN sedes sd ON sd.id_sede = mt.id_sede
        JOIN eval e ON e.id_eval = me.id_eval
        JOIN asignaturas asig ON asig.cod_asig = e.cod_asig
        JOIN alumnos al ON al.rut = mt.rut
        JOIN inscripcion ins ON ins.id_matricula = mt.id_matricula
        JOIN secciones s ON s.id_seccion = ins.id_seccion AND s.cod_asig = e.cod_asig
        where e.num_prueba =0
        ORDER BY 
        sd.nombre_sede,
        asig.cod_asig,
        asig.asig,
        s.seccion
        """

        # Crear un DataFrame con los resultados de la consulta (usando la conexión directa)
        df = pd.read_sql(consulta, conn)

        # Filtrar por 'nombre_sede' y crear un archivo Excel para cada sede
        for nombre_sede, df_sede in df.groupby('nombre_sede'):
            # Crear el nombre del archivo con la sede
            nombre_archivo = f"resultados_sudcra_{nombre_sede}.xlsx"
            ruta_archivo = os.path.join(ruta_convalidados, nombre_archivo)

            # Crear el archivo Excel y guardar los datos de esa sede
            with pd.ExcelWriter(ruta_archivo, mode='w') as writer:
                df_sede.to_excel(writer, index=False, sheet_name=nombre_sede)

            print(f"Archivo generado correctamente para la sede '{nombre_sede}' en: {ruta_archivo}")

    except Exception as e:
        print(f"Error al generar los archivos convalidados: {e}")


# PRUEBAS
ruta_base = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\reportes_sudcra\\2025001\\SEDES\\"
conexion = hace_conexion()
generar_archivos_convalidados(ruta_base, conexion)
cierra_conexion(conexion)

