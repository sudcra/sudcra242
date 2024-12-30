
import datetime
from eval_insert import  hace_conexion , cierra_conexion
from tqdm import tqdm

def agregar_registros(df, tabla_nombre, mensajes):
    mensaje_separador = "-------------------------------------------------------------"
    print(mensaje_separador)
    
    def agregar_mensaje(mensaje):
        mensajes.append(mensaje)

    fecha_hora_inicial = datetime.datetime.now()
    fecha_hora_formateada_inicial = fecha_hora_inicial.strftime("%Y-%m-%d %H:%M:%S")
    mensaje_inicio = f"Inicio del proceso de actualización: tabla {tabla_nombre.upper()}, {fecha_hora_formateada_inicial}"
    agregar_mensaje(mensaje_inicio)
    print(mensaje_inicio)

    conn = hace_conexion()
    
    
    try:
        total_registros = len(df)
        with tqdm(total=total_registros, desc="Progreso") as pbar:
            for index, row in df.iterrows():
                column_names = ', '.join(row.index.tolist())
                values = ', '.join(['%s'] * len(row))

                insert_query = f" INSERT INTO {tabla_nombre} ({column_names}) VALUES ({values})"
                cursor = conn.cursor()                
                try:
                    

                    cursor.execute(insert_query, tuple(row))

                    conn.commit()
                    pbar.update(1)
                    
                except Exception as insert_error:
                    
                    # Log detalles del error para el registro específico
                    mensaje_error_registro = f"Error al insertar el registro {index}: {insert_error}"
                    agregar_mensaje(mensaje_error_registro)
                    print(mensaje_error_registro)
                    #input("Presiona Enter para continuar...")
                    conn.rollback()
                cursor.close()    
        mensaje_exito = f"Datos insertados en la tabla {tabla_nombre} exitosamente."
        mensajes.append(mensaje_exito)
        print(mensaje_exito)

    except Exception as e:
        mensaje_error_general = f"Error al ejecutar la operación: {e}"
        mensajes.append(mensaje_error_general)
        print(mensaje_error_general)
    finally:
        cierra_conexion(conn)

    fecha_hora_final = datetime.datetime.now()
    fecha_hora_formateada_final = fecha_hora_final.strftime("%Y-%m-%d %H:%M:%S")
    mensaje_finaliza_proceso = f"Finaliza el proceso de actualización, {fecha_hora_formateada_final}"
    agregar_mensaje(mensaje_finaliza_proceso)
    print(mensaje_finaliza_proceso)

    diferencia = fecha_hora_final - fecha_hora_inicial
    diferencia_en_minutos = round(diferencia.total_seconds() / 60, 2)

    mensaje_tiempo_utilizado = f"Tiempo utilizado: {diferencia_en_minutos} minutos"
    agregar_mensaje(mensaje_tiempo_utilizado)
    agregar_mensaje(mensaje_separador)
    print(mensaje_tiempo_utilizado)
    print(mensaje_separador)

    return mensajes
