import os
from admin_df_prueba2 import convertir_a_json
import json
import pandas as pd
import sys

import json

def generar_html_docente(data_estudiantes, data_aprendizajes_curso, carpeta_destino, nombre_html):
    # Ruta template vacío de datos
    ruta_template = "C:\\sudcraultra\\sample_vacio.html"
    
    # Leer el HTML vacío
    with open(ruta_template, 'r', encoding='utf-8') as file:
        html_vacio = file.read()

    # Convertir cada fila de los datasets a JSON y unirlas con saltos de línea y coma
    estudiantes_lines = ',\n'.join([json.dumps(row, ensure_ascii=False) for row in data_estudiantes])
    aprendizajes_lines = ',\n'.join([json.dumps(row, ensure_ascii=False) for row in data_aprendizajes_curso])

    # Crear los script con los datos
    script_tag_1 = f'<script>var estudiantes = [\n{estudiantes_lines}\n];</script>'
    script_tag_2 = f'<script>var aprendizajes = [\n{aprendizajes_lines}\n];</script>'
    
    # Insertar los script con los datos en el encabezado del HTML
    html_modificado = html_vacio.replace('</head>', f'{script_tag_1}\n{script_tag_2}</head>', 1)

    # Captura nombre para el archivo html modificado
    seccion = nombre_html

    # Nombre del archivo HTML modificado
    nombre_archivo_modificado = os.path.basename(seccion) + '.html'
    
    # Ruta completa del archivo HTML modificado
    ruta_archivo_modificado = os.path.join(carpeta_destino, nombre_archivo_modificado)

    # Guardar el HTML modificado en un archivo
    with open(ruta_archivo_modificado, 'w', encoding='utf-8') as file:
        file.write(html_modificado)
        print(f"Informe creado: {nombre_archivo_modificado}")

def generar_html_estudiantes(data_estudiantes, data_aprendizajes_estudiantes, data_resultados_sm, data_resultados_ru, data_resultados_de, carpeta_destino):
    # Cargar el JSON data_estudiantes en un DataFrame
    data_estudiantes_df = pd.DataFrame(data_estudiantes)

    # Iterar sobre cada fila del DataFrame
    for index, row in data_estudiantes_df.iterrows():
        # Obtener el nombre y id_matricula_eval del estudiante en el dataset que se esta iterando
        nombre_estudiante = row["nombre_alum"]
        id_matricula_eval = row["id_matricula_eval"]
        if row["tiene_informe"] == 'si' and row["informe_listo"] == False:
            # -------------------------------------------------
            # FILTRO RESULTADOS DE SELECCION MULTIPLE 
            # -------------------------------------------------
            
            # Filtrar los registros donde el campo 'id_matricula_eval' sea igual a id_matricula_eval (del estudiante)
            data_resultados_sm_filtrado = [registro for registro in data_resultados_sm if registro.get('id_matricula_eval') == id_matricula_eval]
            
            # Crear una nueva lista de diccionarios solo con los campos 
            data_resultados_sm_filtrado = [{'item_num': registro['item_num'], 'resultado': registro['resultado']} for registro in data_resultados_sm_filtrado]
            # -------------------------------------------------
            # FILTRO RESULTADOS DE DESARROLLO
            # -------------------------------------------------

            data_resultados_de_filtrado = [registro for registro in data_resultados_de if registro.get('id_matricula_eval') == id_matricula_eval]        
            
            # Crear una nueva lista de diccionarios solo con los campos necesarios
            data_resultados_de_filtrado = [{'item_num': registro['item_num'], 'puntaje_alum': registro['puntaje_alum'], 'item_puntaje': registro['item_puntaje']} for registro in data_resultados_de_filtrado]
            # print(data_resultados_de_filtrado)
            # -------------------------------------------------
            # FILTRO RESULTADOS DE RUBRICA
            # -------------------------------------------------
            
            data_resultados_ru_filtrado = [registro for registro in data_resultados_ru if registro.get('id_matricula_eval') == id_matricula_eval]        
            
            # Crear una nueva lista de diccionarios solo con los campos necesarios
            data_resultados_ru_filtrado = [{'item_num': registro['item_num'], 'item_nombre': registro['item_nombre'], 'nivel_descripcion': registro['nivel_descripcion'], 'puntaje_asignado': registro['puntaje_asignado'], 'item_puntaje': registro['item_puntaje']} for registro in data_resultados_ru_filtrado]
            
            # -------------------------------------------------
            # FILTRO RESULTADOS DE APRENDIZAJE
            # -------------------------------------------------
            
            # Filtrar los registros donde el campo 'id_matricula_eval' sea igual a id_matricula_eval (del estudiante)
            data_aprendizajes_estudiantes_filtrado = [registro for registro in data_aprendizajes_estudiantes if registro.get('id_matricula_eval') == id_matricula_eval]
            
            # Crear una nueva lista de diccionarios solo con los campos
            data_aprendizajes_estudiantes_filtrado = [{'n': registro['n'], 'aprendizaje': registro['aprendizaje'], 'clave': registro['clave'], 'orden': registro['orden'],
            'descripcion_aprendizaje': registro['descripcion_aprendizaje'], 'descripcion_indicador': registro['descripcion_indicador'], 'logro': registro['logro'],
            'logro_prom': registro['logro_prom'], 'nombre_tipo_medida': registro['nombre_tipo_medida'], 'nombre_tipo_medida2': registro['nombre_tipo_medida2'],
            'dimension': registro['dimension'], 'url_retro': registro['url_retro']} for registro in data_aprendizajes_estudiantes_filtrado]
            # -------------------------------------------------
            # DATASET PARA GRAFICO DE DISPERSION (NOTA Y LOGRO)
            # -------------------------------------------------
            # Crear una lista de diccionarios únicamente con las notas de todos los estudiantes excluyendo al estudiante actual
            notas_estudiantes = [{"nota": nota} for nota in data_estudiantes_df[data_estudiantes_df.index != index]["nota"]]
            logros_estudiantes = [{"logro": logro} for logro in data_estudiantes_df[data_estudiantes_df.index != index]["logro_obtenido"]]
            
            # Convertir la lista de diccionarios de notas a JSON y colocarlo entre corchetes
            notas_json = json.dumps(notas_estudiantes)
            logros_json = json.dumps(logros_estudiantes)
            # -------------------------------------------------
            
            
            # -------------------------------------------------
            # OTROS
            # -------------------------------------------------
            # Ruta al template vacío de datos
            ruta_template = "C:\\sudcraultra\\sample-estudiante_vacio.html"
            
            # Leer el HTML vacío
            with open(ruta_template, 'r', encoding='utf-8') as file:
                html_vacio = file.read()

            # Convertir el diccionario del estudiante a JSON y colocarlo entre corchetes (exportar fija actual)
            estudiante_json = json.dumps([row.to_dict()])
            
            # Crear las etiquetas de script con los datos del estudiante, los datos de aprendizaje y las notas del curso
            # script_tag_1 = f'<script>var estudiante = {estudiante_json};</script>'
            script_tag_1 = f'<script>var estudiante = {estudiante_json};</script>'
            script_tag_2 = f'<script>var aprendizajes = {json.dumps(data_aprendizajes_estudiantes_filtrado)};</script>'
            script_tag_3 = f'<script>var resultados_sm = {json.dumps(data_resultados_sm_filtrado)};</script>'
            script_tag_4 = f'<script>var resultados_ru = {json.dumps(data_resultados_ru_filtrado)};</script>'
            script_tag_5 = f'<script>var resultados_de = {json.dumps(data_resultados_de_filtrado)};</script>'
            script_tag_6 = f'<script>var notas_estudiante = {notas_json};</script>'
            script_tag_7 = f'<script>var logros_estudiante = {logros_json};</script>'

            # Insertar las etiquetas de script con los datos en el encabezado del HTML
            html_modificado = html_vacio.replace('</head>', f'{script_tag_1}\n{script_tag_2}\n{script_tag_3}\n{script_tag_4}\n{script_tag_5}\n{script_tag_6}\n{script_tag_7}</head>', 1)

            # Nombre del archivo HTML modificado
            nombre_archivo_modificado = f"{id_matricula_eval}.html"
            
            # Ruta completa del archivo HTML modificado
            ruta_archivo_modificado = os.path.join(carpeta_destino, nombre_archivo_modificado)

            # Guardar el HTML modificado en un archivo
            with open(ruta_archivo_modificado, 'w', encoding='utf-8') as file:
                file.write(html_modificado)
                #print(f"Informe creado: {nombre_archivo_modificado}")
            



if __name__ == "__main__":

    nombre_archivo = "informe"
    carpeta_destino = "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\templates"

    json_estudiantes, json_aprendizajes_estudiantes, json_aprendizajes_curso, json_resultados_sm, json_resultados_ru, json_resultados_de = convertir_a_json()
    
  
    
    generar_html_docente(json_estudiantes, json_aprendizajes_curso, carpeta_destino)
    generar_html_estudiantes(json_estudiantes, json_aprendizajes_estudiantes, json_resultados_sm, json_resultados_ru, json_resultados_de, carpeta_destino)



