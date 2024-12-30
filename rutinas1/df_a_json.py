import pandas as pd

def dataframe_a_json(df):
    try:
        df.columns = df.columns.str.lower()
        
        # Convertir los objetos Timestamp a cadenas de texto en el formato 'YYYY-MM-DD'
        df = df.apply(lambda x: x.map(lambda y: y.strftime('%Y-%m-%d') if isinstance(y, pd.Timestamp) else y))
        
        json_data = df.to_dict(orient='records')
        
    except Exception as e:
        print(f"Error al convertir DataFrame a JSON: {e}")
        json_data = []

    return json_data
