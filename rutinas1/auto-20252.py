import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from crea_informes import crearinformes
from leearchivos import leerarchivos
from envio_mail import camp_alumnos, camp_errores, camp_secciones
from datetime import datetime
from monitor import exporta_monitor
from consultar_ruta_consolidado import consulta_ruta_consolidado

# Lock global
lock = threading.Lock()


class Watcher:
    DIRECTORY_TO_WATCH = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\procesar"

    def __init__(self):
        self.observer = Observer()
        self.last_check = None

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)

                # Ejecutar consulta solo 1 vez por: hora(3600), minuto(60)
                now = datetime.now()
                if not self.last_check or (now - self.last_check).seconds >= 3600:
                    with lock:  # 🔒 Bloquea
                        consulta_ruta_consolidado()
                    self.last_check = now
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            with lock:  # 🔒 Bloquea
                print(f"Archivo creado: {event.src_path}")
                leerarchivos()
                crearinformes()
                camp_errores(1)
                camp_secciones(1)
                camp_alumnos(1)
                try:
                    exporta_monitor()
                except:
                    print("No se logró crear los archivos")
                fecha_hora_actual = datetime.now()
                print("Último proceso:", fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == '__main__':
    w = Watcher()
    w.run()
