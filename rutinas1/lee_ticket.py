import pyodbc
import pandas as pd
import datetime
from eval_insert import hace_conexion, cierra_conexion
from tqdm import tqdm

# Ruta a tu archivo Access
access_db_path = r"C:\Users\lgutierrez\Desktop\Sharepoint.accdb"

# Crear la cadena de conexión para pyodbc
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    fr'DBQ={access_db_path};'
)

# Mapeo de columnas
mapeo_columnas = {
    "ID": "id",
    "Título": "titulo",
    "sede": "sede",
    "Cod_asig": "cod_asig",
    "Seccion": "seccion",
    "Categoría": "categoria",
    "Descripcion": "descripcion",
    "estado": "estado",
    "programa": "programa",
    "Rut": "rut",
    "estado_modificado": "estado_modificado",
    "Datos adjuntos": "datos_adjuntos",
    "Creado": "creado",
    "Creado por": "creado_por"
}

def leer_datos_access(conn_str):
    try:
        conn = pyodbc.connect(conn_str)
        df = pd.read_sql("SELECT * FROM Solicitudes_sudcra", conn)
        conn.close()
        print(df)
        return df
    except Exception as e:
        print("Error al leer los datos:", e)
        return None

def agregar_registros(df, tabla_nombre, mensajes):
    if not isinstance(mensajes, list):
        mensajes = []

    mensaje_separador = "-------------------------------------------------------------"
    print(mensaje_separador)
    
    def agregar_mensaje(mensaje):
        mensajes.append(mensaje)

    fecha_hora_inicial = datetime.datetime.now()
    mensaje_inicio = f"Inicio del proceso de actualización: tabla {tabla_nombre.upper()}, {fecha_hora_inicial.strftime('%Y-%m-%d %H:%M:%S')}"
    agregar_mensaje(mensaje_inicio)
    print(mensaje_inicio)

    conn = hace_conexion()
    
    try:
        # Truncar la tabla antes de insertar nuevos registros
        cursor = conn.cursor()
        cursor.execute(f"TRUNCATE TABLE {tabla_nombre}")
        conn.commit()
        print(f"Tabla {tabla_nombre} truncada exitosamente.")
        
        total_registros = len(df)
        with tqdm(total=total_registros, desc="Progreso") as pbar:
            for index, row in df.iterrows():
                # Filtrar solo las columnas relevantes
                row_filtered = {col: row[col] for col in mapeo_columnas.keys() if col in row}
                
                # Mapear las columnas de acuerdo al mapeo
                mapped_row = {mapeo_columnas.get(col, col): value for col, value in row_filtered.items()}
                
                column_names = ', '.join([f'"{col}"' for col in mapped_row.keys()])
                values = ', '.join(['%s'] * len(mapped_row))

                insert_query = f"INSERT INTO {tabla_nombre} ({column_names}) VALUES ({values})"
                try:
                    cursor.execute(insert_query, tuple(mapped_row.values()))
                    conn.commit()
                    pbar.update(1)
                except Exception as insert_error:
                    mensaje_error_registro = f"Error al insertar el registro {index}: {insert_error}"
                    agregar_mensaje(mensaje_error_registro)
                    print(mensaje_error_registro)
                    conn.rollback()

        mensaje_exito = f"Datos insertados en la tabla {tabla_nombre} exitosamente."
        agregar_mensaje(mensaje_exito)
        print(mensaje_exito)

    except Exception as e:
        mensaje_error_general = f"Error al ejecutar la operación: {e}"
        agregar_mensaje(mensaje_error_general)
        print(mensaje_error_general)
    finally:
        cierra_conexion(conn)

    fecha_hora_final = datetime.datetime.now()
    agregar_mensaje(f"Finaliza el proceso de actualización, {fecha_hora_final.strftime('%Y-%m-%d %H:%M:%S')}")
    diferencia = fecha_hora_final - fecha_hora_inicial
    agregar_mensaje(f"Tiempo utilizado: {round(diferencia.total_seconds() / 60, 2)} minutos")
    agregar_mensaje(mensaje_separador)

    print(mensajes[-3])  # Tiempo utilizado
    print(mensaje_separador)

    return mensajes

# Ejecutar proceso
df = leer_datos_access(conn_str)
if df is not None:
    mensajes = []
    agregar_registros(df, "solicitudes_sudcra", mensajes)
