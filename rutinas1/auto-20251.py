import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from crea_informes import crearinformes
from leearchivos import leerarchivos
from envio_mail import camp_alumnos, camp_errores, camp_secciones
from datetime import datetime, timedelta
from monitor import exporta_monitor
from eval_insert import hace_conexion, cierra_conexion
import os
from log_procesos import crear_tabla_log_procesos
from log_procesos import registrar_inicio_proceso

class Watcher:
    DIRECTORY_TO_WATCH = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\procesar"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

def actualizacion_en_proceso():
    conn = hace_conexion()
    now = datetime.now()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT estado, hora_inicio 
            FROM log_actualizacion 
            WHERE dia = %s AND mes = %s
        """, (now.day, now.month))
        row = cursor.fetchone()

        if not row:
            return False  # No hay actualización registrada hoy

        estado, hora_inicio = row

        if estado != 'En proceso':
            return False

        # Si lleva más de 2 horas en "En proceso", forzamos timeout
        if hora_inicio and (now - hora_inicio) > timedelta(hours=3):
            print("⚠️ Actualización lleva más de 2 horas. Marcando como 'Timeout'.")
            cursor.execute("""
                UPDATE log_actualizacion
                SET estado = 'Timeout'
                WHERE dia = %s AND mes = %s
            """, (now.day, now.month))
            conn.commit()
            return False

        return True  # Sí, aún está en proceso
    except Exception as e:
        print("Error verificando estado de actualización:", e)
        return False
    finally:
        cierra_conexion(conn)

def dentro_de_ventana_actualizacion():
    """Retorna True si estamos dentro de la franja horaria"""
    now = datetime.now().time()
    return now >= datetime.strptime("05:30", "%H:%M").time() and now < datetime.strptime("05:31", "%H:%M").time()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return

        print(f"📂 Archivo creado: {event.src_path}")

        # Validar si está en horario de actualización
        if dentro_de_ventana_actualizacion():
            print("⏳ Dentro de la franja horaria de actualización (05:30 - 05:31n). Esperando...")
            return

        # Validar si hay una actualización en proceso
        while actualizacion_en_proceso():
            print("🔄 Actualización en curso. Esperando 30 segundos...")
            time.sleep(30)

        # Ejecutar rutina principal
        print("✅ Ejecutando procesamiento de archivos...")
        #crear_tabla_log_procesos()
        #registrar_inicio_proceso()
        leerarchivos()
        crearinformes()
        camp_errores(1)
        camp_secciones(1)
        camp_alumnos(1)
        
        try:
            exporta_monitor()
        except:
            print("⚠️ No se logró crear los archivos del monitor")

        fecha_hora_actual = datetime.now()
        print("✅ Último proceso:", fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == '__main__':
    w = Watcher()
    w.run()
