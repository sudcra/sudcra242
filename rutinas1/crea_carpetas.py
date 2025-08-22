#Crea direcctorios con carpetas por sección
import os
from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql
#path_base='C:/SUDCRApy/app/reportes/Consultas/'
sql="SELECT sedes.nombre_sede, asignaturas.programa, asignaturas.cod_asig, secciones.seccion , nombre_doc, apellidos_doc FROM secciones join asignaturas on secciones.cod_asig = asignaturas.cod_asig join sedes on sedes.id_sede = secciones.id_sede join docentes on docentes.rut_docente = secciones.rut_docente  WHERE ASIGNATURAS.cod_asig in ('PLC1101' , 'PLC1110' , 'PLC1301') order by nombre_sede, programa , cod_asig;"
df=ejecutasql(sql)
i=1
for row in df.itertuples():
 #   print(row.id_seccion)
    print(row)
    nueva_carpeta = "C:/sudcraultra_access/carpetas_para_sedes"
    ruta_completa = f"{nueva_carpeta}/P3/{row.programa}/{row.nombre_sede}/{row.cod_asig}/{row.seccion}"
    #ruta_completa = f"{nueva_carpeta}/Test de Competencias/{row.programa}/{row.nombre_sede}/{row.cod_asig}/{row.seccion}"
  
    try:
        os.makedirs(ruta_completa)
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")
    else:
        print("Carpeta creada exitosamente")
    finally:
        print("********")