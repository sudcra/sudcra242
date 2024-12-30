from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql, hace_conexion , cierra_conexion
import pandas as pd
import globales 

def exporta_monitor():
    sql = 'select * from public."BI_AlumnoInscripcion"'
    df1 = ejecutasql(sql)
    ruta = r"C:\Users\lgutierrez\OneDrive - Fundacion Instituto Profesional Duoc UC\SUDCRA\Paneles\\" + globales.globalperiodo + r"\BI_AlumnoInscripcion.csv"
    df1.to_csv(ruta, index=False)
    sql = 'select * from public."BI_Resultados"'
    df2 = ejecutasql(sql)
    ruta = r"C:\Users\lgutierrez\OneDrive - Fundacion Instituto Profesional Duoc UC\SUDCRA\Paneles\\" + globales.globalperiodo + r"\BI_Resultados.csv"
    df2.to_csv(ruta, index=False)

    


if __name__ == "__main__":
    exporta_monitor()