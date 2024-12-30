import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import globales

def mailalum(docente,mail_docente, alumno, mail_alumno, evaluacion, informe, asignatura, seccion, sede):# Configuración de los datos SMTP
    host = "relay.fidelizador.com"
    port = 587  # Puerto típico para TLS
    username = "duocrelay.f017f2+cl1.fidelizador.com"
    password = "74e1e5ed2143d7b539836f7e67439011"
    smtp_secure = 'tls'

    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = "evaluaciones@correos.duoc.cl"
    msg['To'] = mail_alumno
    msg['Subject'] = "Retroalimentación de la evaluación " + evaluacion
    msg.add_header('reply-to', mail_docente)  # Dirección de respuesta

    # Cuerpo del correo en formato HTML
    ruta_archivo_html = 'C:/sudcraultra/templates/cuerpoalum.html'

    # Leer el contenido del archivo HTML y guardarlo en una variable
    with open(ruta_archivo_html, 'r', encoding='utf-8') as archivo_html:
        html = archivo_html.read()


    reemplazos = {"[alumno]": alumno, "[evaluacion]": evaluacion, "[asignatura]": asignatura, "[docente]": docente , "[seccion]": seccion, "[sede]": sede}

    for clave, valor in reemplazos.items():
        html = html.replace(clave, valor)

    msg.attach(MIMEText(html, 'html'))

    # Adjuntar archivo HTML
    ruta_carpeta = "C:/Users/lgutierrez/OneDrive - Fundacion Instituto Profesional Duoc UC/SUDCRA/informes/"+ globales.globalperiodo + "/alumnos/"
    archivo = os.path.join(ruta_carpeta, informe)
    with open(archivo, "rb") as file:
        part = MIMEApplication(file.read(), Name="informe_retroalimentación.html")
    part['Content-Disposition'] = f'attachment; filename="informe_retroalimentación.html"'
    msg.attach(part)

    # Iniciar conexión SMTP
    server = smtplib.SMTP(host, port)
    server.starttls()

    # Autenticación
    server.login(username, password)

    # Enviar correo electrónico
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    # Cerrar conexión SMTP
    server.quit()

    return "¡Correo electrónico enviado correctamente!"


def maildoc(docente,mail_docente,  evaluacion, informe,  seccion, programa,ppt):# Configuración de los datos SMTP
    host = "relay.fidelizador.com"
    port = 587  # Puerto típico para TLS
    username = "duocrelay.f017f2+cl1.fidelizador.com"
    password = "74e1e5ed2143d7b539836f7e67439011"
    smtp_secure = 'tls'

    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = "evaluaciones@correos.duoc.cl"
    msg['To'] = mail_docente
    msg['Subject'] = "Retroalimentación de la evaluación " + evaluacion + ", sección " + seccion
    msg.add_header('reply-to', 'evaluacionestransversales@duoc.cl')  # Dirección de respuesta

    # Cuerpo del correo en formato HTML
    ruta_archivo_html = 'C:/sudcraultra/templates/cuerpo.html'

    # Leer el contenido del archivo HTML y guardarlo en una variable
    with open(ruta_archivo_html, 'r', encoding='utf-8') as archivo_html:
        html = archivo_html.read()



    reemplazos = {"[evaluacion]": evaluacion,  "[docente]": docente , "[seccion]": seccion, "[programa]": programa}

    for clave, valor in reemplazos.items():
        html = html.replace(clave, valor)

    msg.attach(MIMEText(html, 'html'))
    
    # Adjuntar archivo HTML
    ruta_carpeta = "C:/Users/lgutierrez/OneDrive - Fundacion Instituto Profesional Duoc UC/SUDCRA/informes/"+ globales.globalperiodo + "/secciones/"
    archivo = os.path.join(ruta_carpeta,informe)
    with open(archivo, "rb") as file:
        part = MIMEApplication(file.read(), Name="informe.html")
        part['Content-Disposition'] = f'attachment; filename="informe.html"'
        msg.attach(part)

    ruta_carpeta = "C:/Users/lgutierrez/OneDrive - Fundacion Instituto Profesional Duoc UC/SUDCRA/informes/"+ globales.globalperiodo + "/ppts/"
    archivo = os.path.join(ruta_carpeta,ppt)
    try:
        with open(archivo, "rb") as file:
            part = MIMEApplication(file.read(), Name="retro_seccion.pptx")
            part['Content-Disposition'] = f'attachment; filename="retro_seccion.pptx'
            msg.attach(part)
    except:
        print("No hay ppt")

    # Iniciar conexión SMTP
    server = smtplib.SMTP(host, port)
    server.starttls()

    # Autenticación
    server.login(username, password)

    # Enviar correo electrónico
    server.sendmail(msg['From'], msg['To'], msg.as_string())

    # Cerrar conexión SMTP
    server.quit()

    return "¡Correo electrónico enviado correctamente!"

def mailerror(docente,mail_docente,  evaluacion,seccion, imagen, link, eimag, rut, erut, cod_asig, easig, prueba, eprueba, forma, eforma, tipo):# Configuración de los datos SMTP
    host = "relay.fidelizador.com"
    port = 587  # Puerto típico para TLS
    username = "duocrelay.f017f2+cl1.fidelizador.com"
    password = "74e1e5ed2143d7b539836f7e67439011"
    smtp_secure = 'tls'

    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = "evaluaciones@correos.duoc.cl"
    msg['To'] = mail_docente
    msg['Subject'] = "Error de lectura, evaluación " + evaluacion + ", sección " + seccion
    msg.add_header('reply-to', 'evaluacionestransversales@duoc.cl')  # Dirección de respuesta

    # Cuerpo del correo en formato HTML
    ruta_archivo_html = 'C:/sudcraultra/templates/cuerpoerror.html'

    # Leer el contenido del archivo HTML y guardarlo en una variable
    with open(ruta_archivo_html, 'r', encoding='utf-8') as archivo_html:
        html = archivo_html.read()


    reemplazos = {"[evaluacion]": evaluacion,  "[docente]": docente , "[seccion]": seccion , "[imagen]": imagen, "[link]": link, "[estado_imag]": eimag, "[rut]": rut, "[estadorut]": erut, "[cod_asig]": cod_asig, "[estado_asig]": easig, "[prueba]": prueba, "[estado_prueba]": eprueba, "[forma]": forma, "[estado_forma]": eforma, "[tipo]": tipo}

    for clave, valor in reemplazos.items():
        html = html.replace(clave, valor)
    msg.attach(MIMEText(html, 'html'))
    
    try:
    # Iniciar conexión SMTP
        server = smtplib.SMTP(host, port)
        server.starttls()

        # Autenticación
        server.login(username, password)

        # Enviar correo electrónico
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        # Cerrar conexión SMTP
        server.quit()
        mensaje = "correo enviado"
    except:
        mensaje = "no enviado"

    return mensaje

if __name__ == "__main__":
    #print(mailalum('Ronny Godoy', 'lgutierrez@duoc.cl', 'leandro Gutiérrez', 'leander.guty@gmail.com', 'Diagnóstico', '15504151863039032024001.PLC1101-2024001-0.html', 'Nivelación Matemática', 'MAT1111-006V', 'Antonio Varas'))
    #print(maildoc("Ricardo Leal", "lgutierrez@duoc.cl","Diagnóstico","MAT1111-2024001-0_24086890.html","MAT1111-023D", "Programa de matemática"))
    print(maildoc("Leandro Gutiérrez", "lgutierrez@duoc.cl","Diagnóstico","MAT1130-2024002-1_24249523.html","MAT1111-023D", "Programa de matemática","MAT1130-2024002-1_24249523.pptx"))
    #print(mailerror('Katherinnehelen Mondaca Villalon', "lgutierrez@duoc.cl","Diagnóstico", "MAT1111-052V", 'Scan_0039.jpg', "https://duoccl0.sharepoint.com/sites/SUDCRA2/Lists/imgenes/Attachments/25/Scan_0039.jpg", 'OK', '262106390','El rut registrado no es válido', '3','no está inscrito', '0' , 'Ok', '1', 'Ok', 'un error de lectura o de identificación.') )