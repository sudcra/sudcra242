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

def cargar_alumnos(df, tabla_nombre, mensajes):
    """
    Inserta/actualiza alumnos en {tabla_nombre} por clave (rut).
    Requiere columnas: rut, nombres, apellidos, user_alum, sexo.
    Hace upsert en dos pasos para conteos fiables y muestra el resumen
    solo al final, debajo de la barra de progreso.
    """
    req_cols = ["rut", "nombres", "apellidos", "user_alum", "sexo"]
    faltantes = [c for c in req_cols if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el DataFrame: {faltantes}")

    # Trabajar solo con las 5 columnas esperadas y limpiar valores
    base = df[req_cols].copy()
    for c in req_cols:
        base[c] = base[c].map(_to_none_if_nan)

    # Detectar y contar duplicados por rut en el origen (omitidos)
    dups_mask = base.duplicated(subset=["rut"], keep="last")
    omitidos = int(dups_mask.sum())
    # Eliminar duplicados dejando el último
    work = base.drop_duplicates(subset=["rut"], keep="last")

    mensaje_separador = "-------------------------------------------------------------"
    mensajes.append(mensaje_separador)

    fecha_hora_inicial = datetime.datetime.now()
    mensajes.append(
        f"Inicio del proceso de actualización: tabla {tabla_nombre.upper()}, {fecha_hora_inicial:%Y-%m-%d %H:%M:%S}"
    )

    conn = hace_conexion()
    nuevos = 0
    actualizados = 0
    ignorados = 0  # sin cambios
    errores = 0
    errores_detalle = []

    insert_sql = f"""
        INSERT INTO {tabla_nombre} (rut, nombres, apellidos, user_alum, sexo)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (rut) DO NOTHING
        RETURNING 1;
    """

    update_sql = f"""
        WITH datos(rut, nombres, apellidos, user_alum, sexo) AS (
            VALUES (%s, %s, %s, %s, %s)
        )
        UPDATE {tabla_nombre} t
        SET
            nombres   = d.nombres,
            apellidos = d.apellidos,
            user_alum = d.user_alum,
            sexo      = d.sexo
        FROM datos d
        WHERE t.rut = d.rut
          AND (
                t.nombres   IS DISTINCT FROM d.nombres OR
                t.apellidos IS DISTINCT FROM d.apellidos OR
                t.user_alum IS DISTINCT FROM d.user_alum OR
                t.sexo      IS DISTINCT FROM d.sexo
              )
        RETURNING 1;
    """

    try:
        total_registros = len(work)
        with tqdm(total=total_registros, desc="Alumnos") as pbar:
            cur = conn.cursor()
            for idx, row in work.iterrows():
                params = (
                    row["rut"], row["nombres"], row["apellidos"], row["user_alum"], row["sexo"]
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
                    errores_detalle.append({"idx": idx, "rut": row["rut"], "error": str(e)})
                finally:
                    pbar.update(1)
            cur.close()

        # === Resumen final debajo de la barra ===
        print(f"Nuevos: {nuevos}, Actualizados: {actualizados}, Ignorados: {ignorados}, Duplicados en origen: {omitidos}, Errores: {errores}")

        mensajes.append(f"Nuevos: {nuevos}")
        mensajes.append(f"Actualizados: {actualizados}")
        mensajes.append(f"Ignorados (sin cambios): {ignorados}")
        mensajes.append(f"Omitidos (duplicados en origen): {omitidos}")
        mensajes.append(f"Erros: {errores}")

        if errores_detalle:
            # Guarda hasta 10 para referencia en mensajes
            muestras = errores_detalle[:10]
            mensajes.append(f"Ejemplos de errores (máx. 10): {muestras}")

    except Exception as e:
        mensajes.append(f"Error general: {e}")
    finally:
        cierra_conexion(conn)

    fecha_hora_final = datetime.datetime.now()
    mensajes.append(f"Finaliza el proceso: {fecha_hora_final:%Y-%m-%d %H:%M:%S}")
    mensajes.append(f"Tiempo utilizado: {round((fecha_hora_final - fecha_hora_inicial).total_seconds() / 60, 2)} minutos")
    mensajes.append(mensaje_separador)

    return mensajes
