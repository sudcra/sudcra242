from xlsx_a_df import convertir_a_df_tipo_0
from df_a_json import dataframe_a_json
import pandas as pd
import os
import globales


def convertir_fecha(fecha):
    try:
        return pd.to_datetime(fecha, format='%Y-%m-%d')
    except ValueError:
        return pd.to_datetime('1900-01-01')
    
def cargar_datos():
    ruta_calificaciones = "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\consultas_bbdd_ejemplos2\\seccion11.xlsx"
    ruta_aprendizajes_seccion = "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\consultas_bbdd_ejemplos2\\medidas_seccion12.xlsx"
    ruta_aprendizajes_estudiantes = "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\consultas_bbdd_ejemplos2\\medidas_alumnos1.xlsx"
    ruta_resultados_sm= "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\consultas_bbdd_ejemplos2\\item_sm_alumnos1.xlsx"
    ruta_resultados_ru= "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\consultas_bbdd_ejemplos2\\item_ru_alumnos1.xlsx"
    ruta_resultados_de= "C:\\Users\\mcorteze\\Desktop\\Rutinas\\Creando_pdf\\Intento 4\\consultas_bbdd_ejemplos2\\item_de_alumnos1.xlsx"

    df_estudiantes = convertir_a_df_tipo_0(ruta_calificaciones)
    df_aprendizajes_curso = convertir_a_df_tipo_0(ruta_aprendizajes_seccion)
    df_aprendizajes_estudiantes = convertir_a_df_tipo_0(ruta_aprendizajes_estudiantes)
    df_resultados_sm = convertir_a_df_tipo_0(ruta_resultados_sm)
    df_resultados_ru = convertir_a_df_tipo_0(ruta_resultados_ru)
    df_resultados_de = convertir_a_df_tipo_0(ruta_resultados_de)
    
    

    return df_estudiantes, df_aprendizajes_estudiantes, df_aprendizajes_curso, df_resultados_sm, df_resultados_ru, df_resultados_de

def convertir_a_json(df_estudiantes, df_aprendizajes_estudiantes,df_aprendizajes_curso,df_resultados_sm, df_resultados_ru, df_resultados_de):
    # Cargar los datos
    # ------------------------------------------------------------------------------------
    # TRATAMIENTO A DF_ESTUDIANTES
    # ------------------------------------------------------------------------------------
    # Convertir el campo "emision" a tipo datetime con el formato especificado
    #df_estudiantes['lectura_fecha'] = df_estudiantes['lectura_fecha'].apply(convertir_fecha)

    # Cambiar el formato de las fechas a "dd-mm-aaaa"
    try:
        df_estudiantes['lectura_fecha'] = df_estudiantes['lectura_fecha'].dt.strftime('%d-%m-%Y')
    except Exception as e:
        print("Error al formatear la fecha:", e)
        # Intento rescatar el id problematico
       
        #print("ID del registro problematico:", id_registro_problematico)
        print(df_estudiantes['id_seccion'])
        print(df_estudiantes['id_eval'])
        #id_registro_problematico = df_estudiantes.iloc[df_estudiantes['lectura_fecha'].isnull().idxmax()]['id_registro']
    # Cambiar los valores booleanos a 'si' y 'no'
    # Lista de columnas en las que quieres hacer el reemplazo
    columnas_interes_1 = ['rinde', 'tiene_formas', 'tiene_grupo', 'tiene_imagen', 'tiene_planilla', 'tiene_informe', 'tipo_sm','tipo_de', 'tipo_ru', 'ver_correctas']
    columnas_interes_2 = ['nota', 'logro_obtenido']

    # Reemplazar valores en columnas de interés
    df_estudiantes[columnas_interes_1] = df_estudiantes[columnas_interes_1].replace({True: 'si', False: 'no'})
    df_estudiantes[columnas_interes_2] = df_estudiantes[columnas_interes_2].replace({',': '.'})
    # Verificar si el primer valor de 'ver_correctas' es igual a "no"
    """
    if df_estudiantes['ver_correctas'].iloc[0] == 'no':
        # Reemplazar los valores en la columna 'resultado' según la condición dada
        df_resultados_sm['resultado'] = df_resultados_sm['resultado'].replace({'C': 1, 'O': 0, 'E': -1})
    """
    # Función para reemplazar los valores de 'n' con el número de fila + 1
    def reemplazar_valor(row):
        return row.name + 1

    # Aplicamos la función a cada fila utilizando apply()
    df_estudiantes['n'] = df_estudiantes.apply(reemplazar_valor, axis=1)

    # Convertir la columna 'logro_obtenido' a valores numéricos
    df_estudiantes['logro_obtenido'] = pd.to_numeric(df_estudiantes['logro_obtenido'], errors='coerce')

    # Creamos las columnas nota y logro promedio
    # Convertimos la columna 'nota' a valores numéricos
    df_estudiantes['nota'] = pd.to_numeric(df_estudiantes['nota'], errors='coerce')

    df_estudiantes['nota_prom'] = round(df_estudiantes['nota'].mean(), 1)
    df_estudiantes['logro_obtenido_prom'] = round(df_estudiantes['logro_obtenido'].mean(), 3)

    ruta_ondrive_base = 'https://duoccl0-my.sharepoint.com/personal/lgutierrez_duoc_cl/Documents/SUDCRA/informes/'+ globales.globalperiodo + '/alumnos/'
    df_estudiantes['informe'] = ruta_ondrive_base  + df_estudiantes['id_matricula_eval'].astype(str)+'.html'
 
    # FINALIZA EL TRATAMIENTO A DF ESTUDIANTES 
    
    # ------------------------------------------------------------------------------------
    # TRATAMIENTO A DF_APRENDIZAJES_SECCION
    # ------------------------------------------------------------------------------------
    # Aplicar una función lambda a la columna 'orden' para generar la nueva columna 'aprendizaje'
    df_aprendizajes_curso['aprendizaje'] = df_aprendizajes_curso['orden'].apply(lambda x: f'Aprendizaje {x}')
    df_aprendizajes_curso['dimension'] = df_aprendizajes_curso.apply(lambda row: f"{row['nombre_tipo_medida']} {row['orden']}", axis=1)
    # Creando el campo clave
    # Se ordena el DataFrame por la columna 'orden'
    df_aprendizajes_curso = df_aprendizajes_curso.sort_values(by='orden')
    # Se inicializa un contador para el correlativo
    correlativo = 1
    claves = []
    # Se itera sobre cada fila del DataFrame
    for index, row in df_aprendizajes_curso.iterrows():
        # Se genera la clave concatenando la letra 'a', el valor de 'orden' y el correlativo
        clave = f"a{row['orden']}{correlativo}"
        # Se agrega la clave a la lista
        claves.append(clave)
        
        # Se verifica si el valor de 'orden' cambió respecto al siguiente registro
        if index + 1 < len(df_aprendizajes_curso) and row['orden'] != df_aprendizajes_curso.loc[index + 1, 'orden']:
            # Si cambió, se reinicia el correlativo
            correlativo = 1
        else:
            # Si no cambió, se incrementa el correlativo
            correlativo += 1

    # Se agrega la lista de claves como una nueva columna al DataFrame
    df_aprendizajes_curso['clave'] = claves # Quedó listo, facil y bonito, ejaleeeee
    
    # Creamos el campo n el cual es un duplicado del campo orden
    df_aprendizajes_curso['n'] = df_aprendizajes_curso['orden'].copy()


    # Supongamos que tienes un DataFrame llamado df con una columna llamada 'nombre_antiguo'
    # y deseas cambiar el nombre de esta columna a 'nombre_nuevo'

    df_aprendizajes_curso.rename(columns={'desc_larga': 'descripcion_aprendizaje'}, inplace=True)
    df_aprendizajes_curso.rename(columns={'desc_larga2': 'descripcion_indicador'}, inplace=True)
    df_aprendizajes_curso.rename(columns={'logro': 'logro_prom'}, inplace=True)
    df_aprendizajes_curso.rename(columns={'logro2': 'logro'}, inplace=True)

    # Formateamos los decimales
    df_aprendizajes_curso['logro_prom'] = df_aprendizajes_curso['logro_prom'].apply(lambda x: round(x * 100, 1))
    df_aprendizajes_curso['logro'] = df_aprendizajes_curso['logro'].apply(lambda x: round(x * 100, 1))


    # ------------------------------------------------------------------------------------
    # TRATAMIENTO A DF_APRENDIZAJES_ESTUDIANTE
    # ------------------------------------------------------------------------------------
    # Aplicar una función lambda a la columna 'orden' para generar la nueva columna 'aprendizaje'
    df_aprendizajes_estudiantes['aprendizaje'] = df_aprendizajes_estudiantes['orden'].apply(lambda x: f'Aprendizaje {x}')
    df_aprendizajes_estudiantes['dimension'] = df_aprendizajes_estudiantes.apply(lambda row: f"{row['nombre_tipo_medida']} {row['orden']}", axis=1)  
    # Creando el campo clave
    # Se ordena el DataFrame por la columna 'orden'
    df_aprendizajes_estudiantes = df_aprendizajes_estudiantes.sort_values(by='orden')

    # Se inicializa un contador para el correlativo
    correlativo = 1
    claves = []
    # Se itera sobre cada fila del DataFrame
    for index, row in df_aprendizajes_estudiantes.iterrows():
        # Se genera la clave concatenando la letra 'a', el valor de 'orden' y el correlativo
        clave = f"a{row['orden']}{correlativo}"
        # Se agrega la clave a la lista
        claves.append(clave)
        
        # Se verifica si el valor de 'orden' cambió respecto al siguiente registro
        if index + 1 < len(df_aprendizajes_estudiantes) and row['orden'] != df_aprendizajes_estudiantes.loc[index + 1, 'orden']:
            # Si cambió, se reinicia el correlativo
            correlativo = 1
        else:
            # Si no cambió, se incrementa el correlativo
            correlativo += 1

    # Se agrega la lista de claves como una nueva columna al DataFrame
    df_aprendizajes_estudiantes['clave'] = claves # Quedó listo, facil y bonito, ejaleeeee
    
    # Creamos el campo n el cual es un duplicado del campo orden
    df_aprendizajes_estudiantes['n'] = df_aprendizajes_estudiantes['orden'].copy()


    # Supongamos que tienes un DataFrame llamado df con una columna llamada 'nombre_antiguo'
    # y deseas cambiar el nombre de esta columna a 'nombre_nuevo'

    df_aprendizajes_estudiantes.rename(columns={'desc_larga': 'descripcion_aprendizaje'}, inplace=True)
    df_aprendizajes_estudiantes.rename(columns={'desc_larga2': 'descripcion_indicador'}, inplace=True)
    df_aprendizajes_estudiantes.rename(columns={'logro': 'logro_prom'}, inplace=True)
    df_aprendizajes_estudiantes.rename(columns={'logro2': 'logro'}, inplace=True)

    # Formateamos los decimales
    df_aprendizajes_estudiantes['logro_prom'] = df_aprendizajes_estudiantes['logro_prom'].apply(lambda x: round(x * 100, 1))
    df_aprendizajes_estudiantes['logro'] = df_aprendizajes_estudiantes['logro'].apply(lambda x: round(x * 100, 1))

    # Reemplazar en todo el DataFrame
    df_estudiantes = df_estudiantes.replace('', '-')
    df_estudiantes = df_estudiantes.fillna("-")

    # ------------------------------------------------------------------------------------
    # TRATAMIENTO A DF_RESULTADOS_ALTERNATIVAS
    # ------------------------------------------------------------------------------------
    
    df_resultados_sm['resultado'] = df_resultados_sm['resultado'].replace({'C': 'Correcta', 'E': 'Incorrecta', 'O': 'Omitida'})
    

    try:
        json_estudiantes = dataframe_a_json(df_estudiantes)
        json_aprendizajes_estudiantes = dataframe_a_json(df_aprendizajes_estudiantes)
        json_aprendizajes_curso = dataframe_a_json(df_aprendizajes_curso)
        json_resultados_sm = dataframe_a_json(df_resultados_sm)
        json_resultados_ru = dataframe_a_json(df_resultados_ru)
        json_resultados_de = dataframe_a_json(df_resultados_de)
        
    except Exception as e:
        print(f"Error al convertir DataFrame a JSON: {e}")
        return None, None, None

    return json_estudiantes, json_aprendizajes_estudiantes, json_aprendizajes_curso, json_resultados_sm, json_resultados_ru, json_resultados_de



    
