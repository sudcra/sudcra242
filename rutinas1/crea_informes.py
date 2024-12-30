
from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql, hace_conexion , cierra_conexion
from admin_df_prueba2 import convertir_a_json
from admin_4 import generar_html_docente, generar_html_estudiantes
from agrega_registros import agregar_registros
from datetime import datetime, timezone
import pandas as pd
import psycopg2
from psycopg2 import sql
from crea_pptx import creappt
from tqdm import tqdm
import globales 

def crearinformes():
    path_base='C:/sudcraultra/Consultas/'
    # Consula SQL tabla informes_secciones_pendientes
    sql='SELECT * FROM informes_secciones_pendientes'
    df=ejecutasql(sql)
    # Consulta SQL tabla 

    i=1
    total_registros = len(df)
    with tqdm(total=total_registros, desc="Progreso informes secciones") as pbar:
        for row in df.itertuples():
            
            
            if row.num_prueba == 0:
                medida="UC"      
            else:
                medida="AE"     
            archivo = open(path_base + 'listado_seccion_eval.sql', "r")
            sql= archivo.read()

            sql = sql.replace("[id_seccion]", str(row.id_seccion))
            sql = sql.replace("[id_eval]", row.id_eval)

            df_estudiantes=ejecutasql(sql) #df es el listado sección
            
            #df_estudiantes.to_excel('seccion'+str(i)+'.xlsx', index=False) 
            if not df_estudiantes.empty:
            # ---------------------------
            #       Creación PPT
            # ---------------------------
                if row.retro_doc == True:
                    archivo = open(path_base + 'item_evalseccionmenos.sql', "r")
                    sql= archivo.read()

                    sql = sql.replace("[id_seccion]", str(row.id_seccion))
                    sql = sql.replace("[id_eval]", row.id_eval)
                    sql = sql.replace("[n]", str(row.num_ppt))

                    df_itemesmenos=ejecutasql(sql) #df es el listado sección
                    

                    # Instanciamos
                    itemesmenos=[]
                
                    idSeccion = row.id_seccion
                    nombrePpt = row.id_eval + ".pptx"
                    nombrePptNuevo = row.id_eval + '_' + str(row.id_seccion) + ".pptx"
                    nombreEvaluacion = df_estudiantes['nombre_prueba'].iloc[0]
                    nombreSeccion = df_estudiantes['seccion'].iloc[0]
                    nombreProfesor = df_estudiantes['docente'].iloc[0]

                    for itemes in df_itemesmenos.itertuples():
                        itemesmenos.append(itemes.item_orden) 
                
                    # Creamos el ppt llamando a la función
                    creappt(nombrePpt,nombrePptNuevo,nombreEvaluacion, nombreSeccion, nombreProfesor, itemesmenos)
                


                archivo = open(path_base + 'medidas_seccion_eval.sql', "r")
                sql= archivo.read()
                sql = sql.replace("[id_seccion]", str(row.id_seccion))
                sql = sql.replace("[id_eval]", row.id_eval)
                sql = sql.replace("[medida]", medida) 
                df_aprendizajes_curso=ejecutasql(sql) #df2 medidas de la sección
                
                #df_aprendizajes_curso.to_excel('medidas_seccion'+str(i)+'.xlsx', index=False)

                archivo = open(path_base + 'medidas_seccion_eval_matricula.sql', "r")
                sql= archivo.read()
                sql = sql.replace("[id_seccion]", str(row.id_seccion))
                sql = sql.replace("[id_eval]", row.id_eval)
                sql = sql.replace("[medida]", medida) 
                df_aprendizajes_estudiantes=ejecutasql(sql)
                #df3 medidas de alumnos de la seccion
                #df_aprendizajes_estudiantes.to_excel('medidas_alumnos'+str(i)+'.xlsx', index=False)

                archivo = open(path_base + 'itemsm_alum_eval.sql', "r")
                sql= archivo.read()
                sql = sql.replace("[id_seccion]", str(row.id_seccion))
                sql = sql.replace("[id_eval]", row.id_eval)
                df_resultados_sm=ejecutasql(sql) #itemes SM de los alumnos
                
                #df_resultados_sm.to_excel('item_sm_alumnos'+str(i)+'.xlsx', index=False)

                archivo = open(path_base + 'itemru_alum_eval.sql', "r")
                sql= archivo.read()
                sql = sql.replace("[id_seccion]", str(row.id_seccion))
                sql = sql.replace("[id_eval]", row.id_eval)
                df_resultados_ru=ejecutasql(sql)  #df5 itemes RU de los alumnos
                
                #df_resultados_ru.to_excel('item_ru_alumnos'+str(i)+'.xlsx', index=False)

                archivo = open(path_base + 'itemde_alum_eval.sql', "r")
                sql= archivo.read()
                sql = sql.replace("[id_seccion]", str(row.id_seccion))
                sql = sql.replace("[id_eval]", row.id_eval)
                df_resultados_de=ejecutasql(sql)  #df6 itemes DE de los alumnos
                
                #df_resultados_de.to_excel('item_de_alumnos'+str(i)+'.xlsx', index=False)
                
                carpeta_seccion = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\informes\\" + globales.globalperiodo +  "\\secciones"
                carpeta_alumnos = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\\SUDCRA\\informes\\" + globales.globalperiodo +  "\\alumnos"

                json_estudiantes, json_aprendizajes_estudiantes, json_aprendizajes_curso, json_resultados_sm, json_resultados_ru, json_resultados_de = convertir_a_json(df_estudiantes, df_aprendizajes_estudiantes,df_aprendizajes_curso,df_resultados_sm, df_resultados_ru, df_resultados_de)
                #print(json_aprendizajes_curso)   
                
                html_seccion = row.id_eval + "_" + str(row.id_seccion)
                generar_html_docente(json_estudiantes, json_aprendizajes_curso, carpeta_seccion, html_seccion)

                fecha_hora_actual = datetime.now()
                print( fecha_hora_actual )
                data = {
                'id_seccion': [ str(row.id_seccion)],
                'id_eval': [row.id_eval],
                'marca_temporal': [fecha_hora_actual]
                }

            # Crear un DataFrame a partir del diccionario
                dfinformeseccion = pd.DataFrame(data)

                agregar_registros(dfinformeseccion,'informes_secciones',[])


                generar_html_estudiantes(json_estudiantes, json_aprendizajes_estudiantes, json_resultados_sm, json_resultados_ru, json_resultados_de, carpeta_alumnos)
                
                # Filtrar df por el campo informe_listo igual a False
                df_filtered = df_estudiantes[df_estudiantes['informe_listo'] == False]

                # Crear dfalum a partir del campo id_matricula_eval del DataFrame filtrado
                dfalum = df_filtered[['id_matricula_eval']].copy()
                dfalum['marca_temporal'] = pd.Timestamp.now()
                agregar_registros(dfalum,'informe_alumnos',[])

                conexion = hace_conexion()
                cursor = conexion.cursor()
                # Iterar sobre las filas del DataFrame y actualizar la base de datos
                for index, row in dfalum.iterrows():
                    # Actualizar el campo informe_listo en la tabla calificaciones_obtenidas
                    update_query = "UPDATE calificaciones_obtenidas SET informe_listo = true WHERE id_matricula_eval = %s"
                    cursor.execute(update_query, (row['id_matricula_eval'],))
                
                # Confirmar los cambios
                conexion .commit() 
                cierra_conexion(conexion)  
                pbar.update(1)

            i=i+1

if __name__ == "__main__":
    crearinformes()