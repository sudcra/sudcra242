from ruta_archivo import obtener_ruta_archivo
from xlsx_a_df import convertir_a_df_tipo_0 , convertir_a_df_tipo_1
import pandas as pd

ruta = obtener_ruta_archivo()


data = pd.read_csv(ruta, sep='\t', header=None, encoding='latin1')

# Omitir las filas 1, 2, 3 y 5
data = data.drop([1, 2, 3, 5])

# Omitir la primera columna
data = data.drop(columns=0)

# Mostrar los datos resultantes
print(data)