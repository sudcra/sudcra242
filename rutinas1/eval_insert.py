from xlsx_a_df import convertir_a_df_tipo_0
import psycopg2
from datetime import datetime, timezone
from ruta_archivo import obtener_ruta_archivo
import pandas as pd
import datetime
import os
from sqlalchemy import create_engine
from tqdm import tqdm

def hace_conexion():
  #  """Establece una conexión con la base de datos PostgreSQL."""
    try:
        # Cambia los valores según tu configuración de la base de datos
        conn = psycopg2.connect(
            database="sudcra",
            user="postgres",
            password="fec4a5n5",
            host="localhost",
            port="5432"
        )
        # print("Conexión establecida correctamente.")
        return conn
    except psycopg2.Error as e:
        print(f"Error al establecer la conexión: {e}")
        return None


def cierra_conexion(conn):
  #  """Cierra la conexión con la base de datos."""
    try:
        if conn:
            conn.close()
            # print("Conexión cerrada correctamente.")
        else:
            print("No hay conexión para cerrar.")
    except psycopg2.Error as e:
        print(f"Error al cerrar la conexión: {e}")


#******************************************************************************
def inserta_eval(ruta):
    nombre_hoja="eval"
    df=convertir_a_df_tipo_0(ruta, nombre_hoja)
    campos_eval = df.iloc[0].to_dict()
 #   print(campos_eval)

    # Crea una conexión a la base de datos
    conexion = hace_conexion()
    '''
    conexion = psycopg2.connect(
            database="SUDCRA",
            user="postgres",
            password="fec4a5n5",
            host="localhost",
            port="5432"
    )
    '''
    # Desactiva el modo de confirmación automática
    conexion.autocommit = False


    # inserción en tabla eval":
    try:
        fecha_hora_actual = datetime.datetime.now()
        with conexion.cursor() as cursor:
            id_eval = campos_eval['id_eval']
            cod_asig = campos_eval['cod_asig']
            ano = campos_eval['ano']
            periodo = campos_eval['periodo']
            num_prueba = campos_eval['num_prueba']
            nombre_prueba = campos_eval['nombre_prueba']
            tiene_formas = campos_eval['tiene forma']
            retro_alum = campos_eval['retro_alum']
            retro_doc = campos_eval['retro_doc']
            ver_correctas= campos_eval['ver_correcta']
            tiene_grupo =  campos_eval['tiene_grupo']
            archivo_tabla =  campos_eval['archivo']
            cargado_fecha = fecha_hora_actual
            exigencia = campos_eval['exigencia']
            num_ppt = campos_eval['num_ppt']
            ponderacion = campos_eval['ponderacion']
            tipo = campos_eval['tipo_eval']

            consulta = "INSERT INTO eval (id_eval , cod_asig, ano, periodo, num_prueba, nombre_prueba, tiene_formas, retro_alum, retro_doc, ver_correctas, tiene_grupo, archivo_tabla, cargado_fecha, exigencia, num_ppt, ponderacion, tipo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(consulta, (id_eval, cod_asig, ano, periodo, num_prueba, nombre_prueba, tiene_formas, retro_alum, retro_doc, ver_correctas, tiene_grupo, archivo_tabla, cargado_fecha, exigencia, num_ppt, ponderacion, tipo))
            resultado= "Registro insertado correctamente"
            # No olvides hacer commit para guardar los cambios
            conexion.commit()
    except Exception as e:
        resultado= f"Error al insertar el registro: {e}"
        print(resultado)
    finally:
        cierra_conexion(conexion)
        cod=campos_eval['cod_asig']
        prueba=campos_eval['num_prueba']
        return cod, prueba, resultado

def crea_df_item_respuesta(df, cod_asig, prueba):
    conn = hace_conexion()
    
    cursor = conn.cursor()
    cursor.execute("SELECT cod_interno FROM asignaturas WHERE cod_asig = %s;", (cod_asig,))
    codigo_interno = cursor.fetchone()
    print(codigo_interno)
    dfir = pd.DataFrame(columns=['id_itemresp', 'id_item', 'registro', 'puntaje_asignado'])
    n=0
    for index, row in df.iterrows():
        match row['item_tipo']:
            case "SM":
                for i in range(6):
                    anoperiodo=str(row['id_item'])[:7]
                    idir = anoperiodo + codigo_interno[0] + str(prueba).zfill(2)+ str(row['forma']).zfill(2)+ str(row['item_orden']).zfill(3) + str(i)
                    idi = row['id_item']
                    reg = i                   
                    match i:
                        case 0:
                            puntaje=0
                        case 1:
                            if row['correccion'] == "A":
                               puntaje=1
                            else:
                               puntaje=0
                        case 2:
                            if row['correccion'] == "B":
                               puntaje=1
                            else:
                               puntaje=0
                        case 3:
                            if row['correccion'] == "C":
                               puntaje=1
                            else:
                               puntaje=0
                        case 4:
                            if row['correccion'] == "D":
                               puntaje=1
                            else:
                               puntaje=0
                        case 5:
                            if row['correccion'] == "E":
                               puntaje=1
                            else:
                               puntaje=0   
                        case _:
                           puntaje=0
                    # Crear una nueva fila
                    #nueva_fila = {'id_item_resp':idir, 'id_item': idi, 'registro': reg , 'puntaje_asignado': puntaje}
                    nueva_fila = [idir, idi,  reg ,  puntaje]
                    #print(nueva_fila)
                    # Agregar la fila al DataFrame
                    #dfir= dfir.append(nueva_fila, ignore_index=True)
                    dfir.loc[n] = nueva_fila
                    n += 1

            case "RU":
                cadenaCorreccion=row["correccion"].replace(",", ".")
                punt_ru=cadenaCorreccion.split(";")
                ran=len(punt_ru)+1
                for i in range(ran):
                    if punt_ru[i-1] != '':
                        anoperiodo=str(row['id_item'])[:7]
                        idir = anoperiodo + codigo_interno[0] + str(prueba).zfill(2)+ str(row['forma']).zfill(2)+ str(row['item_orden']).zfill(3) + str(i)
                        idi = row['id_item']
                        reg = i
                        if i==0:
                            puntaje=0
                        else:
                            if len(punt_ru) >= i:
                                puntaje = float(punt_ru[i-1])
                            else:
                                puntaje = 0
                        
                        # Crear una nueva fila
                        nueva_fila = [idir, idi,  reg ,  puntaje]
                        #print(nueva_fila)
                        # Agregar la fila al DataFrame
                        dfir.loc[n] = nueva_fila
                        n += 1
            case "DE":
                
                anoperiodo=str(row['id_item'])[:7]
                
                idir = anoperiodo + codigo_interno[0] + str(prueba).zfill(2)+ str(row['forma']).zfill(2)+ str(row['item_orden']).zfill(3)
                idi = row['id_item']
                reg = 0
                puntaje=row["correccion"]
                # Crear una nueva fila
                nueva_fila = [idir, idi,  reg ,  puntaje]
                #print(nueva_fila)
                # Agregar la fila al DataFrame
                dfir.loc[n] = nueva_fila
                n += 1

    print(n)     
    return dfir   



def inserta_archivo(ruta):
    
 #   print(campos_eval)

    # Crea una conexión a la base de datos
    conexion = hace_conexion()
      # Desactiva el modo de confirmación automática
    conexion.autocommit = False
    fecha_hora = datetime.datetime.now()
    

    # inserción en tabla eval":
    try:
       
        with conexion.cursor() as cursor:
            archivo, tipoarchivo = os.path.splitext(ruta)    
            archivoleido = archivo + tipoarchivo
            estadolectura = "leyendo"
            observacion = "na"
            marcatemporal =  fecha_hora
            consulta = "INSERT INTO archivosleidos (archivoleido , tipoarchivo, estadolectura, observacion, marcatemporal) VALUES (%s, %s, %s, %s, %s) RETURNING id_archivoleido"
            cursor.execute(consulta, (archivoleido , tipoarchivo, estadolectura, observacion, marcatemporal))
            id_archivo = cursor.fetchone()[0]
            resultado= "Registro insertado correctamente"
            # No olvides hacer commit para guardar los cambios
            conexion.commit()
    except Exception as e:
        resultado= f"Error al insertar el registro: {e}"
    finally:
        cierra_conexion(conexion)
        
        return resultado, id_archivo




def txt_a_df(ruta, anoperiodo , id_archivoleido):
    df = pd.DataFrame(columns=['rut', 'id_itemresp', 'id_archivoleido', 'linea_leida', 'reproceso', 'imagen', 'instante_forms', 'num_prueba', 'forma','grupo', 'cod_interno', 'registro_leido'])
    df2 = pd.DataFrame(columns=['rut', 'id_itemresp', 'id_archivoleido', 'linea_leida', 'reproceso', 'imagen', 'instante_forms', 'num_prueba', 'forma','grupo', 'cod_interno', 'registro_leido'])
    
    with open(ruta, "r") as archivo:
    # Lee cada línea del archivo
        
        linea_leida = 1
        n=0
        
        
        
        for linea in tqdm(archivo, desc="Procesando archivo", unit="linea"):
            #    Divide la línea en una lista de valores
            datos = linea.strip().split(",")
            if datos[0]=='1':
                rep= True
            else:
                rep = False
            imag = os.path.basename(datos[1])

            fecha_str = datos[2] # Formato: aammdd
            hora_str = datos[3]  # Formato: hhmmss

                # Convertir las cadenas en objetos datetime
            fecha_dt = datetime.datetime.strptime(fecha_str, "%y%m%d")
            hora_dt = datetime.datetime.strptime(hora_str, "%H%M%S")

                # Combinar fecha y hora
            fecha_hora_forms = fecha_dt.replace(hour=hora_dt.hour, minute=hora_dt.minute, second=hora_dt.second)
            mapeo = {
                "00": "0",
                "01": "1",
                "02": "2",
                "03": "3",
                "04": "4",
                "05": "5",
                "06": "6",
                "07": "7",
                "08": "8",
                "09": "9",
                "10": "K",
                "0":"",
                "  ":" "
            }
            #print("************************************************************************************************************")
            
            rut= mapeo.get(datos[4],datos[4])+datos[5]+datos[6]+datos[7]+datos[8]+datos[9]+datos[10]+datos[11]+ mapeo.get(datos[12])
            asig = datos[13]
            prueba = datos[14]
            forma = datos[15]
            item = 1
            if linea_leida%100 == 0 and linea_leida != 0:
                df= pd.concat([df, df2], ignore_index=True)
                df2=df2.drop(df2.index)
            for reg in datos[16:]:
                if reg == " " or reg == "":
                    regi="0"
                else:
                    regi=reg

                id_itemresp = anoperiodo + str(asig) + str(prueba).zfill(2) + str(forma).zfill(2) + str(item).zfill(3) + regi
                nueva_fila = [rut, id_itemresp, id_archivoleido, linea_leida, rep, imag, fecha_hora_forms, prueba, forma, 1 , asig, regi]
                df2.loc[n] = nueva_fila
                nueva_fila = None
                
                item += 1
                n += 1
            linea_leida +=1
            pass
        df= pd.concat([df, df2], ignore_index=True)
        df2=df2.drop(df2.index)
    return df



def ejecutasqlarch(ruta):
   
 #   print(campos_eval)
   # path_to_sql_file = 'ruta/al/archivo.sql'

# Leer el contenido del archivo
    with open(ruta, 'r') as sql_file:
        sql_query = sql_file.read()
        
    # Crea una conexión a la base de datos
    conexion = hace_conexion()
      # Desactiva el modo de confirmación automática
    conexion.autocommit = False
     # inserción en tabla eval":
    try:
       
        with conexion.cursor() as cursor:
            cursor.execute(sql_query)
            conexion.commit()
    # Obtener los resultados (si es necesario)
            resultado = "consulta realizada"
            
            
            # No olvides hacer commit para guardar los cambios
            
    except Exception as e:
        resultado= f"Error al insertar el registro: {e}"
    finally:
        cierra_conexion(conexion)
        
        return resultado     

def ejecutasql2(sql):
   
    
    # Crea una conexión a la base de datos
    conexion = hace_conexion()
      # Desactiva el modo de confirmación automática
    conexion.autocommit = False

    df = pd.read_sql_query(sql, conexion)    

    cierra_conexion(conexion)
        
    return df  

def ejecutasql(consulta):
    # Establecer conexión a la base de datos
    engine = create_engine('postgresql://postgres:fec4a5n5@localhost/sudcra')
    conexion = engine.connect()
    
    try:
        # Ejecutar la consulta SQL y obtener los resultados
        df = pd.read_sql_query(consulta, conexion)
        return df
    finally:
        # Cerrar la conexión a la base de datos
        conexion.close()
