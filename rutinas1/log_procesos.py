from eval_insert import hace_conexion, cierra_conexion
from datetime import datetime

def crear_tabla_log_procesos():
    """ Crea la tabla log_procesos si no existe """
    conn = hace_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_procesos (
                mes INT NOT NULL,
                dia INT NOT NULL,
                hora_inicio TIMESTAMP,
                PRIMARY KEY (mes, dia)
            )
        """)
        conn.commit()
    except Exception as e:
        print("Error al crear la tabla log_procesos:", e)
    finally:
        cierra_conexion(conn)

def registrar_inicio_proceso():
    """ Registra la hora de inicio de un proceso """
    conn = hace_conexion()
    now = datetime.now()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO log_procesos (mes, dia, hora_inicio)
            VALUES (%s, %s, %s)
            ON CONFLICT (mes, dia) DO UPDATE 
            SET hora_inicio = EXCLUDED.hora_inicio
        """, (now.month, now.day, now))
        conn.commit()
        print(f"Inicio del proceso registrado a las {now.strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        print("Error al registrar el inicio del proceso:", e)
    finally:
        cierra_conexion(conn)
