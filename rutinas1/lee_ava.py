import pandas as pd
import re
def xlsava_a_df(ruta, anoperiodo, id_archivoleido):

    control = 0
    try:
        with open(ruta, 'r') as file:
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
                'respuesta': df1.iloc[:, 7].str[:29].str.replace('\x00', '').str.replace('"', '')
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

if __name__ == "__main__":
    archivo = 'C:\\sudcraultra_access\\testeo_AVA\\MAT4120.xls'
    df= xlsava_a_df(archivo, "2024002" , 23)
    print(df)    