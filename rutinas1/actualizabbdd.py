import pyodbc
import pandas as pd
from agrega_registros import agregar_registros

def actualizabd():
    db_path = r'C:\sudcraultra\access\actualizasudcra.accdb'

    # Conecta a la base de datos
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + db_path)
    # Consulta SQL

    

    # Ejecuta la consulta
    cursor = conn.cursor()

    query = "SELECT * FROM asignatura"
    cursor.execute(query)

    # Lee los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)
    #print(df)
    nombre_tabla = 'asignaturas'
    agregar_registros(df,nombre_tabla,[])
   
    """query = "SELECT * FROM alumnos "
    cursor.execute(query)

    # Lee los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)
    #print(df)
    nombre_tabla = 'alumnos'
    agregar_registros(df,nombre_tabla,[])


    query = "SELECT * FROM docentes "
    cursor.execute(query)
    # Lee los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)
    #print(df)
    nombre_tabla = 'docentes'
    agregar_registros(df,nombre_tabla,[])

    query = "SELECT * FROM matricula "
    cursor.execute(query)
    # Lee los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)
    #print(df)
    nombre_tabla = 'matricula_a'
    agregar_registros(df,nombre_tabla,[])


    query = "SELECT * FROM secciones "
    cursor.execute(query)
    # Lee los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)
    #print(df)
    nombre_tabla = 'secciones_a'
    agregar_registros(df,nombre_tabla,[])

    query = "SELECT * FROM inscripcion3 "
    cursor.execute(query)
    # Lee los resultados en un DataFrame
    df = pd.read_sql_query(query, conn)
    #print(df)
    nombre_tabla = 'inscripcion_a'
    agregar_registros(df,nombre_tabla,[])
"""
    # Cierra la conexión
    
    conn.close()

    # Ahora puedes trabajar con el DataFrame 'df'
    

if __name__ == "__main__":
    actualizabd()