import pandas as pd
import chardet
import re
from datetime import datetime
def xlsava_a_df(ruta, anoperiodo, id_archivoleido):

    control = 0
    try:
        with open(ruta, 'rb') as rawdata:
            result = chardet.detect(rawdata.read(100000))
        detected_encoding = result['encoding']
        confidence = result['confidence']   
        if detected_encoding:
            if confidence < 0.8 and detected_encoding not in ['utf-8', 'utf-16', 'latin-1']:
                print("Advertencia: La confianza de la detección es baja. Intentando con UTF-8 como fallback.")
                actual_encoding = 'utf-8'
            else:
                actual_encoding = detected_encoding

        with open(ruta, 'r', encoding=actual_encoding) as file:
            lines = file.readlines()
        df1 = pd.DataFrame(
            [(i + 1, *line.strip().split('\t')) for i, line in enumerate(lines[1:])],
            columns=['Número de Línea'] + lines[0].strip().split('\t')
        )
    except Exception as e2:
        print(f"Error leyendo el archivo de texto: {e2}")
        try:
            df1 = pd.read_excel(ruta)
            df1.insert(0, 'Número de Registro', range(1, len(df1) + 1))
            control = 1
            print("Archivo leído con éxito usando pd.read_excel.")
        except Exception as e3:
            print(f"Error leyendo el archivo Excel: {e3}")
            return pd.DataFrame()  # Retorna un DataFrame vacío si ambos métodos fallan

    try:
        # Procesamiento del DataFrame
        df1 = df1.dropna(subset=[df1.columns[5]])

        if control == 1:
            nuevo_df = pd.DataFrame({
                'user_alum': df1.iloc[:, 1].str.upper().str.replace('\x00', '').str.replace('"', ''),
                'rep': df1.iloc[:, 2].str.replace('\x00', '').str.replace('"', ''),
                'num': df1.iloc[:, 5].apply(lambda x: str(x).replace('\x00', '').replace('"', '') if isinstance(x, str) else x),
                'id_item': df1.iloc[:, 6].str[:2000].str.replace('"', ''),
                'registroa': df1.iloc[:, 9],
                'registrom': df1.iloc[:, 10],
                'id_archivoleido': id_archivoleido,
                'linea_leida': df1.iloc[:, 0],
                'respuesta': df1.iloc[:, 7].str[:13].str.replace('\x00', '').str.replace('"', '')
            })
        else:
            nuevo_df = pd.DataFrame({
                'user_alum': df1.iloc[:, 1].str.upper().str.replace('\x00', '').str.replace('"', ''),
                'rep': df1.iloc[:, 2].str.replace('\x00', '').str.replace('"', ''),
                'num': df1.iloc[:, 5].str.replace('\x00', '').str.replace('"', ''),
                'id_item': df1.iloc[:, 6].str[:2000].str.replace('"', ''),
                'registroa': df1.iloc[:, 9].str.replace('\x00', '').str.replace('"', '').str.replace(',', '.'),
                'registrom': df1.iloc[:, 10].str.replace('\x00', '').str.replace('"', '').str.replace(',', '.'),
                'id_archivoleido': id_archivoleido,
                'linea_leida': df1.iloc[:, 0],
                'respuesta': df1.iloc[:, 7].str[:13].str.replace('\x00', '').str.replace('"', '')
            })

        nuevo_df = nuevo_df[nuevo_df[nuevo_df.columns[2]].apply(lambda x: str(x).strip() if isinstance(x, str) else x) != ""]
        nuevo_df = nuevo_df.drop(columns=["num"])
        nuevo_df = nuevo_df[nuevo_df['id_item'].notnull() & (nuevo_df['id_item'] != "")]
        nuevo_df['registroa'] = pd.to_numeric(nuevo_df['registroa'], errors='coerce')
        nuevo_df['registrom'] = pd.to_numeric(nuevo_df['registrom'], errors='coerce')
        nuevo_df['registroa'] = nuevo_df['registroa'].fillna(0)
        if len(str(nuevo_df['id_item'].iloc[0]).split('|')) > 1:
           nuevo_df['id_item'] = nuevo_df['id_item'].astype(str).str.split('|').str[1]
        else:
           nuevo_df['id_item'] = nuevo_df['id_item'].str[:36].str.replace('"', '')   

        nuevo_df['id_item'] = nuevo_df['id_item'].apply(lambda x: re.sub(r'[^\d\s]', '', x).lstrip().split(' ')[0])

        return nuevo_df
    except Exception as e:
        print(f"Error procesando el DataFrame: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío si falla el procesamiento


import pandas as pd
import numpy as np 

def crear_dataframe_desde_excel(ruta_archivo: str, id_archivoleido):
    """
    Lee un archivo de Excel, lo procesa para generar un DataFrame con una
    estructura de salida específica y lógica condicional según 'tipo_pregunta'.

    Args:
        ruta_archivo (str): La ruta completa donde se encuentra el archivo de Excel.
        id_archivoleido: Un identificador que se asignará a cada fila del resultado.

    Returns:
        pandas.DataFrame: Un DataFrame con la estructura final, o None si ocurre un error.
    """
    # Columnas necesarias del archivo original, incluyendo 'tipo_pregunta'
    columnas_requeridas = [
        'rut',
        'pregunta_acarreo_id',
        'seleccionadas',
        'nota_manual',
        'nota_automatica',
        'user_id',
        'tipo_pregunta'  # <--- COLUMNA AÑADIDA
    ]

    try:
        df = pd.read_excel(ruta_archivo, dtype={'rut': str})
        print(f"✅ ¡Archivo Excel leído exitosamente desde: {ruta_archivo}!")

        # Verificar si todas las columnas requeridas existen
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        if columnas_faltantes:
            print(f"❌ Error: Las siguientes columnas no se encontraron en el archivo: {columnas_faltantes}")
            return None
        
        # 1. Crear DataFrame de trabajo y columnas básicas
        df_trabajo = df[columnas_requeridas].copy()
        df_trabajo['linea_leida'] = df.index + 1
        df_trabajo['reproceso'] = np.where(df_trabajo['user_id'].str.lower() == 'r', True, False)
        
        # 2. Dividir el DataFrame según 'tipo_pregunta'
        df_multiples = df_trabajo[df_trabajo['tipo_pregunta'] == 'Selección múltiple'].copy()
        df_otras = df_trabajo[df_trabajo['tipo_pregunta'] != 'Selección múltiple'].copy()
        print(f"✅ ¡DataFrame dividido: {len(df_multiples)} filas de 'Selección múltiple' y {len(df_otras)} de otros tipos!")

        # 3. Procesar y expandir solo las filas de 'Selección múltiple'
        if not df_multiples.empty:
            df_multiples['seleccionadas'] = df_multiples['seleccionadas'].astype(str).fillna('').replace('nan', '')
            df_multiples['seleccionadas'] = df_multiples['seleccionadas'].str.split(',')
            df_multiples = df_multiples.explode('seleccionadas')
            df_multiples['seleccionadas'] = df_multiples['seleccionadas'].str.strip()
            print("✅ ¡Filas de 'Selección múltiple' expandidas!")

        # 4. Unir los dos DataFrames de nuevo
        df_expandido = pd.concat([df_multiples, df_otras], ignore_index=True)

        # 5. Crear identificadores y puntajes con la nueva lógica
        # La concatenación solo ocurre si el tipo es 'Selección múltiple' Y hay algo seleccionado
        condicion_concat = (df_expandido['tipo_pregunta'] == 'Selección múltiple') & (df_expandido['seleccionadas'].astype(str).str.strip() != '')
        id_pregunta = df_expandido['pregunta_acarreo_id'].astype(str)
        id_seleccion = df_expandido['seleccionadas'].astype(str)
        
        df_expandido['id_itemresp'] = np.where(condicion_concat, id_pregunta + '_' + id_seleccion, id_pregunta)
        
        df_expandido['puntaje_alum'] = np.where(
            df_expandido['nota_manual'].notna(), 
            df_expandido['nota_manual'], 
            df_expandido['nota_automatica']
        )
        print("✅ ¡Columna 'id_itemresp' creada con la nueva lógica!")

        # 6. Construir el DataFrame final
        instante_creacion = datetime.now()
        df_final = pd.DataFrame({
            'rut': df_expandido['rut'],
            'id_itemresp': df_expandido['id_itemresp'],
            'id_archivoleido': id_archivoleido,
            'linea_leida': df_expandido['linea_leida'],
            'reproceso': df_expandido['reproceso'],
            'registro_leido': df_expandido['puntaje_alum'].round(3),
            'instante_forms': instante_creacion
        })
        print("✅ ¡DataFrame final construido exitosamente!")
        
        return df_final

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en la ruta: {ruta_archivo}")
        return None
    except ImportError:
        print("❌ Error: La librería 'openpyxl' es necesaria. Instálala con: pip install openpyxl")
        return None
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
        return None



if __name__ == "__main__":
    archivo = 'C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\SUDCRA\\procesar\\test3.xlsx'
    df = crear_dataframe_desde_excel(archivo,23)
    #df= xlsava_a_df(archivo, "2024002" , 23)
    nombre_archivo_salida = "C:\\Users\\lgutierrez\\OneDrive - Fundacion Instituto Profesional Duoc UC\SUDCRA\\procesar\\datos_procesados.csv"
    df.to_csv(nombre_archivo_salida, index=False, sep=';', encoding='utf-8-sig')
    
    print(f"\n✅ ¡DataFrame exportado exitosamente a {nombre_archivo_salida}!")

    print(df)    