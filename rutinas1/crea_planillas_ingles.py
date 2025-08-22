from eval_insert import txt_a_df , inserta_archivo, ejecutasqlarch, ejecutasql, hace_conexion , cierra_conexion
from admin_df_prueba2 import convertir_a_json
from admin_4 import generar_html_docente, generar_html_estudiantes
from agrega_registros import agregar_registros
from datetime import datetime, timezone
import pandas as pd
import psycopg2
from psycopg2 import sql
from crea_pptx import creappt
import xlsxwriter
from tqdm import tqdm
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.workbook.protection import WorkbookProtection
import os

# Parámetros globales
ANIO = 2025
PERIODO = '002'
CARPETAONDRIVE = 'IMR20252'

def copiasPlanillas(archivox, cod_asig, carpeta, sufijo, idseccion, fil , col):
    raiz, extension = os.path.splitext(archivox)
    path_base='C:/sudcraultra/Consultas/'

    archivo = open(path_base + 'listado_planillas.sql', "r")
    sql= archivo.read()
    if idseccion == "":
        sql = sql.replace("[seccion]", '')
    else:
        sql = sql.replace("[seccion]", 'AND s.id_seccion = ' + idseccion)

    sql = sql.replace("[cod_asig]", cod_asig)
    df=ejecutasql(sql)
    total_registros = len(df)
    with tqdm(total=total_registros, desc=f"Progreso planillas {cod_asig}-{sufijo}") as pbar:
        for row in df.itertuples():
            archivo = open(path_base + 'listado_alumnos_planillas.sql', "r")
            sql= archivo.read()
            sql = sql.replace("[id_seccion]", str(row.id_seccion))
            dfa=ejecutasql(sql)
            ruta_completa = f"{carpeta}/{row.cod_programa}/{row.cod_sede}/{sufijo}/{cod_asig}"
            try:
                os.makedirs(ruta_completa, exist_ok=True)
            except Exception:
                pass
            
            seccion = f"{row.cod_sede}_{row.seccion}"
            new_planilla = f"{carpeta}/{row.cod_programa}/{row.cod_sede}/{sufijo}/{cod_asig}/{seccion}_{sufijo}{extension}"
            dfAplanilla(dfa, archivox, new_planilla, fil, col, seccion)
            pbar.update(1)

def dfAplanilla(df, excel_file, new_excel_file, start_row, start_col, seccion):
    wb = load_workbook(filename=excel_file, read_only=False, keep_vba=True)
    if "SECCION" in wb.sheetnames:
        wb["SECCION"].title = seccion

    ws = wb.active

    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=False), start=start_row):
        for c_idx, value in enumerate(row, start=start_col):
            ws.cell(row=r_idx, column=c_idx, value=value)

    for fila in range(start_row + len(df), start_row + 60):
        ws.row_dimensions[fila].hidden = True

    ws.protection.sheet = True
    ws.protection.set_password('arcdus')

    try:
        wsh = wb["Hoja1"]
        wsh.sheet_state = 'hidden'
    except KeyError:
        pass

    wb.security = WorkbookProtection(workbookPassword='arcdus', lockStructure=True)

    wb.save(new_excel_file)
    wb.close()

def ejecutar_planillas_ingles(lista_cod_asig, ruta_base, carpeta_destino):
    for cod_asig in lista_cod_asig:
        for prueba, sufijo in [ (2, 'Ev2')]:
            archivo = f"{cod_asig}-{ANIO}{PERIODO}-{prueba}.xlsm"
            rutaArchivo = os.path.join(ruta_base, archivo)
            print(f"Procesando {cod_asig}, prueba {prueba} con sufijo {sufijo}")
            copiasPlanillas(rutaArchivo, cod_asig, carpeta_destino, sufijo, "", 7, 2)

if __name__ == "__main__":
    lista_ingles = [
        'MAI2121'
    ]

    ruta_base = f'C:/sudcraultra_access/SISTEMA/planillas_base/'
    carpeta_destino = f'C:/Users/lgutierrez/OneDrive - Fundacion Instituto Profesional Duoc UC/SUDCRA/PLANILLAS/{CARPETAONDRIVE}'

    ejecutar_planillas_ingles(lista_ingles, ruta_base, carpeta_destino)
