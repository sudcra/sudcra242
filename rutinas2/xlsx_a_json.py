import pandas as pd
import json

def xlsx_a_json(excel_path):
    try:
        df = pd.read_excel(excel_path)
        df.columns = df.columns.str.lower()
        
        # Convertir los objetos Timestamp a cadenas de texto en el formato 'DD-MM-YYYY'
        df = df.apply(lambda x: x.dt.strftime('%d-%m-%Y') if pd.api.types.is_datetime64_any_dtype(x) else x)
        
        data = df.to_dict(orient='records')
        # No es necesario convertir los datos a JSON aquí, ya que la conversión se hará después en el bucle principal.
        
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        data = []

    return data
