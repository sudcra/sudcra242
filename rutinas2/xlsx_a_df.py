import pandas as pd

# Convierte a df la hoja activa de un libro excel con extensión .xlsx
# El df se genera a partir de la región escrita en la planilla.

def convertir_a_df_tipo_0(ruta):
    # Carga de archivos XLSX a DataFrames
    df = pd.read_excel(ruta)

    # Rellenar los valores NaN con una cadena vacía
    df = df.fillna('')

    return df

# Convierte a df una hoja de un libro excel con extensión .xlsx
# Requiere especificar: nombre de la hoja y coordenadas de la región

def convertir_a_df_tipo_1(ruta, nombre_hoja, f_inicial, f_final, c_inicial, c_final):
    # Carga de archivo XLSX a DataFrame
    df = pd.read_excel(ruta, sheet_name=nombre_hoja)

    # Recortar el DataFrame usando coordenadas
    df_recortado = df.iloc[f_inicial-1:f_final, c_inicial-1:c_final]

    # Rellenar los valores NaN con una cadena vacía en el DataFrame recortado
    df_recortado = df_recortado.fillna('')

    return df_recortado

# Convierte a df la hoja activa de un libro excel con extensión .xlsx
# Requiere especificar: coordenadas de la región

def convertir_a_df_tipo_2(ruta, f_inicial, f_final, c_inicial, c_final):
    # Carga de archivos XLSX a DataFrames
    df = pd.read_excel(ruta)

    # Recortar el DataFrame usando las coordenadas proporcionadas
    df_recortado = df.iloc[f_inicial-1:f_final, c_inicial-1:c_final]
     
    df_recortado = df_recortado.fillna('')
    
    return df_recortado