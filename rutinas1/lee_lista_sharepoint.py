import pyodbc
import pandas as pd
from agrega_registros import agregar_registros

def imagenes_list(ultimo_leido):
    db_path = r'C:\sudcraultra_access\lista.accdb'
    conn = None  # Define la conexión fuera del bloque try
    try:
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_path)
        query = f"SELECT * FROM hojas WHERE id_lista > {ultimo_leido}"
        cursor = conn.cursor()
        cursor.execute(query)
        df = pd.read_sql_query(query, conn)
        print(df)
        nombre_hoja = 'imagenes'
        agregar_registros(df, nombre_hoja, [])
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(f"Hubo un error al ejecutar la consulta: {sqlstate}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Asegura que la conexión se cierre
        if conn is not None:
            conn.close()
if __name__ == "__main__":
    imagenes_list(2576)