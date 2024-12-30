import psycopg2

def hace_conexion():
  #  """Establece una conexión con la base de datos PostgreSQL."""
    try:
        # Cambia los valores según tu configuración de la base de datos
        conn = psycopg2.connect(
            database="sudcra",
            user="postgres",
            password="fec4a5n5",
            host="localhost",
            port="5432"
        )
        print("Conexión establecida correctamente.")
        return conn
    except psycopg2.Error as e:
        print(f"Error al establecer la conexión: {e}")
        return None
 
 
def cierra_conexion(conn):
  #  """Cierra la conexión con la base de datos."""
    try:
        if conn:
            conn.close()
            print("Conexión cerrada correctamente.")
        else:
            print("No hay conexión para cerrar.")
    except psycopg2.Error as e:
        print(f"Error al cerrar la conexión: {e}")