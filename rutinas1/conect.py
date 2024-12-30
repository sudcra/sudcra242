import psycopg2

try:
    # Conexión a la base de datos
    conexion = psycopg2.connect(
        database="sudcra",
        user="postgres",
        password="fec4a5n5",
        host="localhost",
        port="5432"
    )

    # Crear un cursor
    cursor = conexion.cursor()

    # Ejecutar una consulta SQL
    cursor.execute("SELECT * FROM tipo_medida")

    # Obtener los resultados
    resultados = cursor.fetchall()

    #Imprimir los resultados
    for fila in resultados:
        print(fila)

except Exception as e:
    print(f"Ha ocurrido un error al conectar a la base de datos: {e}")
finally:




    if conexion:
        cursor.close()
        conexion.close()
