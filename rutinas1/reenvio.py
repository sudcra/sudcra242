from eval_insert import inserta_eval , crea_df_item_respuesta, hace_conexion , cierra_conexion, ejecutasql
from ruta_archivo import obtener_ruta_archivo
from xlsx_a_df import convertir_a_df_tipo_0 , convertir_a_df_tipo_1
from agrega_registros import agregar_registros
from mail import maildoc
from tqdm import tqdm

def cargaReenvios():
    ruta = obtener_ruta_archivo()


    nombre_hoja="t_reenvioinformesseccion"
    df = convertir_a_df_tipo_0(ruta, nombre_hoja)

    agregar_registros(df,nombre_hoja,[])

def reenvio():
    path_base='C:/sudcraultra/Consultas/'
    # Consula SQL tabla informes_secciones_pendientes
    sql="select * from reenvio_seccion"
    df=ejecutasql(sql)
    # Consulta SQL tabla 

    i=1
    total_registros = len(df)
    with tqdm(total=total_registros, desc="Progreso informes secciones") as pbar:
        for row in df.itertuples():
            maildoc(row.nombre_destinatario, row.mail_destinatario,row.nombre_prueba,row.informe,row.seccion, row.programa,row.ppt)
            pbar.update(1)
            
if __name__ == "__main__":
    cargaReenvios()
    reenvio()