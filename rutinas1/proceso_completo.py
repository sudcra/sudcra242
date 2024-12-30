from crea_informes import crearinformes
from leearchivos import leerarchivos
from envio_mail import camp_alumnos, camp_errores, camp_secciones
from datetime import datetime
from monitor import exporta_monitor

leerarchivos()
crearinformes()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
camp_errores(1)
camp_secciones(1)
camp_alumnos(1)
exporta_monitor()
fecha_hora_actual = datetime.now()
print("Último proceso:", fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"))
