from mail import mailalum,maildoc,mailerror
from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql, hace_conexion , cierra_conexion
from datetime import datetime, timezone
import msvcrt
from tqdm import tqdm

def esperar_tecla():
    print("Presiona una tecla para continuar o ESC para salir...")
    tecla = msvcrt.getch()
    return tecla

def camp_errores(test):
    sql='SELECT * FROM mail_error'
    df=ejecutasql(sql)
    conexion = hace_conexion()
    cursor = conexion.cursor()
    total_registros = len(df)
    with tqdm(total=total_registros, desc="Progreso mail error") as pbar:
        for row in df.itertuples():
            
            
            #mailerror(row.docente,'mcorteze@duoc.cl',row.evaluacion,row.seccion,row.imagen,row.url_imagen,row.eimag,row.rut,row.erut,row.cod_asig,row.easig,row.nombre_prueba,row.eprueba,str(row.forma),row.eforma,row.tipo)
            mailerror(row.docente,row.mail,row.evaluacion,row.seccion,row.imagen,row.url_imagen,row.eimag,row.rut,row.erut,row.cod_asig,row.easig,row.nombre_prueba,row.eprueba,row.forma,row.eforma,row.tipo)
            pbar.update(1)
            if test==1:
                fecha_hora_actual = datetime.now()
                update_query = "UPDATE errores SET mail_enviado = true , marca_temp_mail = %s  WHERE id_error = %s"
                cursor.execute(update_query, (fecha_hora_actual,row.id_error))
                conexion .commit() 
            if test!=1:
                tecla = esperar_tecla()
                if tecla == b'\x1b':  # Verificar si la tecla presionada es ESC
                    print("Saliendo...")
                    break
                else:
                    print("Tecla presionada:", tecla)
            
    cierra_conexion(conexion)  

def camp_alumnos(test):
    sql='SELECT * FROM mail_alum'
    df=ejecutasql(sql)
    conexion = hace_conexion()
    cursor = conexion.cursor()
    total_registros = len(df)
    with tqdm(total=total_registros, desc="Progreso mail alumnos") as pbar:
        for row in df.itertuples():
            
            #mailalum(row.docente,row.mail_doc, row.alumno, "lgutierrez@duoc.cl", row.nombre_prueba, row.informe, row.asig, row.seccion, row.sede)
            mailalum(row.docente,row.mail_doc, row.alumno, row.mail_alum, row.nombre_prueba, row.informe, row.asig, row.seccion, row.sede)
            pbar.update(1)
            if test==1:
                fecha_hora_actual = datetime.now()
                update_query = "UPDATE informe_alumnos SET mail_enviado = true , marca_temp_mail = %s  WHERE id_informealum = %s"
                cursor.execute(update_query, (fecha_hora_actual,row.id_informealum))
                conexion .commit() 
            if test!=1:
                tecla = esperar_tecla()
                if tecla == b'\x1b':  # Verificar si la tecla presionada es ESC
                    print("Saliendo...")
                    break
                else:
                    print("Tecla presionada:", tecla)
        
    cierra_conexion(conexion)  

def camp_secciones(test):
    sql='SELECT * FROM mail_seccion'
    df=ejecutasql(sql)
    conexion = hace_conexion()
    cursor = conexion.cursor()
    total_registros = len(df)
    with tqdm(total=total_registros, desc="Progreso mail secciones") as pbar:
        for row in df.itertuples():
            ppt = row.informe.replace('html' , 'pptx')
            #mensaje=maildoc(row.docente,"lgutierrez@duoc.cl",row.nombre_prueba,row.informe, row.seccion,row.programa)
            mensaje=maildoc(row.docente,row.mail_doc,row.nombre_prueba,row.informe, row.seccion,row.programa,ppt)
            pbar.update(1)
            if test==1:
                fecha_hora_actual = datetime.now()
                update_query = "UPDATE informes_secciones SET mail_enviado = true , marca_temp_mail = %s  WHERE id_informeseccion = %s"
                cursor.execute(update_query, (fecha_hora_actual,row.id_informeseccion))
                conexion .commit() 
            if test!=1:
                tecla = esperar_tecla()
                if tecla == b'\x1b':  # Verificar si la tecla presionada es ESC
                    print("Saliendo...")
                    break
                else:
                    print("Tecla presionada:", tecla)
            
    cierra_conexion(conexion)  

if __name__ == "__main__":
    camp_errores(1)
    camp_secciones(1)
    camp_alumnos(1)