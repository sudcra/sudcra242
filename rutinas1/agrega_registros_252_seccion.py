import datetime
from eval_insert import hace_conexion, cierra_conexion
from tqdm import tqdm

def _to_none_if_nan(v):
    # Convierte NaN/None/"" a None y trimea strings
    try:
        import pandas as pd
        if v is None or (isinstance(v, float) and v != v) or (hasattr(pd, "isna") and pd.isna(v)):
            return None
    except Exception:
        pass
    if isinstance(v, str):
        v = v.strip()
        return v if v != "" else None
    return v

def cargar_secciones(df, tabla_nombre, mensajes):
    """
    Inserta/actualiza registros en {tabla_nombre} (p.ej. 'secciones') por clave primaria id_seccion.
    Requiere columnas en el DataFrame:
      id_seccion, cod_asig, num_seccion, jornada, id_sede, rut_docente, ano, periodo, seccion
    NO incluye ninguna columna ni lógica de 'vigente'.
    Upsert en dos pasos para conteos fiables. Resumen al final, sin postfix en tqdm.
    """
    req_cols = [
        "id_seccion", "cod_asig", "num_seccion", "jornada", "id_sede",
        "rut_docente", "ano", "periodo", "seccion"
    ]
    faltantes = [c for c in req_cols if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el DataFrame: {faltantes}")

    # Trabajar solo con las columnas esperadas y limpiar valores
    base = df[req_cols].copy()
    for c in req_cols:
        base[c] = base[c].map(_to_none_if_nan)

    # Detectar y contar duplicados por id_seccion en el origen (omitidos)
    dups_mask = base.duplicated(subset=["id_seccion"], keep="last")
    omitidos = int(dups_mask.sum())
    # Eliminar duplicados dejando el último
    work = base.drop_duplicates(subset=["id_seccion"], keep="last")

    mensaje_separador = "-------------------------------------------------------------"
    mensajes.append(mensaje_separador)

    t0 = datetime.datetime.now()
    mensajes.append(
        f"Inicio del proceso de actualización: tabla {tabla_nombre.upper()}, {t0:%Y-%m-%d %H:%M:%S}"
    )

    conn = hace_conexion()
    nuevos = 0
    actualizados = 0
    ignorados = 0  # sin cambios
    errores = 0
    errores_detalle = []

    insert_sql = f"""
        INSERT INTO {tabla_nombre} (
            id_seccion, cod_asig, num_seccion, jornada, id_sede,
            rut_docente, ano, periodo, seccion
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (id_seccion) DO NOTHING
        RETURNING 1;
    """

    update_sql = f"""
        WITH datos(id_seccion, cod_asig, num_seccion, jornada, id_sede, rut_docente, ano, periodo, seccion) AS (
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        )
        UPDATE {tabla_nombre} t
        SET
            cod_asig    = d.cod_asig,
            num_seccion = d.num_seccion,
            jornada     = d.jornada,
            id_sede     = d.id_sede,
            rut_docente = d.rut_docente,
            ano         = d.ano,
            periodo     = d.periodo,
            seccion     = d.seccion
        FROM datos d
        WHERE t.id_seccion = d.id_seccion
          AND (
                t.cod_asig    IS DISTINCT FROM d.cod_asig OR
                t.num_seccion IS DISTINCT FROM d.num_seccion OR
                t.jornada     IS DISTINCT FROM d.jornada OR
                t.id_sede     IS DISTINCT FROM d.id_sede OR
                t.rut_docente IS DISTINCT FROM d.rut_docente OR
                t.ano         IS DISTINCT FROM d.ano OR
                t.periodo     IS DISTINCT FROM d.periodo OR
                t.seccion     IS DISTINCT FROM d.seccion
              )
        RETURNING 1;
    """

    try:
        total_registros = len(work)
        with tqdm(total=total_registros, desc="Secciones:") as pbar:
            cur = conn.cursor()
            for idx, row in work.iterrows():
                params = (
                    row["id_seccion"], row["cod_asig"], row["num_seccion"], row["jornada"], row["id_sede"],
                    row["rut_docente"], row["ano"], row["periodo"], row["seccion"]
                )
                try:
                    # 1) Intento de INSERT
                    cur.execute(insert_sql, params)
                    ins = cur.fetchone()
                    if ins:
                        nuevos += 1
                    else:
                        # 2) Intento de UPDATE si no insertó
                        cur.execute(update_sql, params)
                        upd = cur.fetchone()
                        if upd:
                            actualizados += 1
                        else:
                            ignorados += 1  # ya existía exactamente igual
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    errores += 1
                    errores_detalle.append({"idx": idx, "id_seccion": row["id_seccion"], "error": str(e)})
                finally:
                    pbar.update(1)
            cur.close()

        # === Resumen final debajo de la barra ===
        print(f"Nuevos: {nuevos}, Actualizados: {actualizados}, Ignorados: {ignorados}, Duplicados en origen: {omitidos}, Errores: {errores}")

        mensajes.append(f"Nuevos: {nuevos}")
        mensajes.append(f"Actualizados: {actualizados}")
        mensajes.append(f"Ignorados (sin cambios): {ignorados}")
        mensajes.append(f"Omitidos (duplicados en origen): {omitidos}")
        mensajes.append(f"Errores: {errores}")

        if errores_detalle:
            # Guarda hasta 10 para referencia
            muestras = errores_detalle[:10]
            mensajes.append(f"Ejemplos de errores (máx. 10): {muestras}")

    except Exception as e:
        mensajes.append(f"Error general: {e}")
    finally:
        cierra_conexion(conn)

    t1 = datetime.datetime.now()
    mensajes.append(f"Finaliza el proceso: {t1:%Y-%m-%d %H:%M:%S}")
    mensajes.append(f"Tiempo utilizado: {round((t1 - t0).total_seconds() / 60, 2)} minutos")
    mensajes.append(mensaje_separador)
    return mensajes
