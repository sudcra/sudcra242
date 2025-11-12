from datetime import datetime, timedelta
from eval_insert import hace_conexion, cierra_conexion
from carga_tabla_actualiza_porRuta import carga_tabla_actualiza


def consulta_ruta_consolidado():
    conn = hace_conexion()
    now = datetime.now()
    hoy = now.date()
    ayer = hoy - timedelta(days=1)

    dia_hoy = str(hoy.day).zfill(2)
    mes_hoy = str(hoy.month).zfill(2)
    dia_ayer = str(ayer.day).zfill(2)
    mes_ayer = str(ayer.month).zfill(2)

    try:
        cursor = conn.cursor()

        # 1. ¿Ya hay registro de HOY completado?
        cursor.execute("""
            SELECT 1
            FROM log_actualizacion
            WHERE estado = 'Completado'
              AND carga = 'Completado'
              AND dia = %s AND mes = %s
            LIMIT 1
        """, (dia_hoy, mes_hoy))
        if cursor.fetchone():
            print(">>> Actualización de BBDD: Ya existe registro de actualización de hoy. No es necesario procesar más.")
            return

        # 2. Buscar primero uno pendiente de HOY
        cursor.execute("""
            SELECT id, ruta_consolidado, dia, mes
            FROM log_actualizacion
            WHERE estado = 'Completado'
              AND carga = 'Preparado'
              AND dia = %s AND mes = %s
            ORDER BY hora_inicio DESC
            LIMIT 1
        """, (dia_hoy, mes_hoy))
        row = cursor.fetchone()

        # 3. Si no hay de hoy, buscar en AYER
        if not row:
            cursor.execute("""
                SELECT id, ruta_consolidado, dia, mes
                FROM log_actualizacion
                WHERE estado = 'Completado'
                  AND carga = 'Preparado'
                  AND dia = %s AND mes = %s
                ORDER BY hora_inicio DESC
                LIMIT 1
            """, (dia_ayer, mes_ayer))
            row = cursor.fetchone()

        # 4. Procesar si hay registro
        if row:
            id_registro, ruta, dia_reg, mes_reg = row
            print(">>> -------------------------------------------------")
            print(f">>> Actualización de BBDD: Archivo listo para procesar: {ruta} (fecha {dia_reg}/{mes_reg})")

            try:
                print(">>> Actualización de BBDD: Iniciando actualización...")
                print(">>> -------------------------------------------------")
                carga_tabla_actualiza(ruta)

                # 5. Marcar como Completado si no hubo error
                cursor.execute("""
                    UPDATE log_actualizacion
                    SET carga = 'Completado'
                    WHERE id = %s
                """, (id_registro,))
                conn.commit()

                print(f">>> Actualización de BBDD: Registro id:{id_registro} marcado como Completado ✅")

            except FileNotFoundError:
                print(f">>> Actualización de BBDD: Error - No se encontró el archivo en la ruta {ruta}")
                print(">>> -------------------------------------------------")
            except Exception as e:
                print(f">>> Actualización de BBDD: Error al procesar archivo {ruta}:", e)
                print(">>> -------------------------------------------------")

        else:
            print(">>> Actualización de BBDD: No se encontró registro pendiente para actualización (ni de hoy ni de ayer).")

    except Exception as e:
        print(">>> Actualización de BBDD: Error en la consulta:", e)

    finally:
        cierra_conexion(conn)
