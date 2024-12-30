import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from crea_informes import crearinformes
from leearchivos import leerarchivos
from envio_mail import camp_alumnos, camp_errores, camp_secciones
from datetime import datetime
from monitor import exporta_monitor

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


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Aquí se ejecuta la rutina cuando se crea un archivo nuevo
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
