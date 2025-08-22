import datetime
from eval_insert import hace_conexion, cierra_conexion
from tqdm import tqdm

def _to_none_if_nan(v, lower=False):
    """
    Convierte NaN/None/"" a None y trimea strings.
    Si lower=True, además pasa a minúsculas (para username/mail).
    """
    try:
        import pandas as pd
        if v is None:
            return None
        # NaN de float
        if isinstance(v, float) and v != v:
            return None
        # NaN de pandas
        if hasattr(pd, "isna") and pd.isna(v):
            return None
    except Exception:
        pass

    if isinstance(v, str):
        s = v.strip()
        if s == "":
            return None
        if lower:
            s = s.lower()
        return s
    return v

def cargar_docentes(df, tabla_nombre, mensajes):
    """
    Inserta/actualiza docentes en {tabla_nombre} por clave (rut_docente).
    Requiere columnas: rut_docente, nombre_doc, apellidos_doc, username_doc, mail_doc.
    Realiza upsert en dos pasos para conteos confiables y muestra el resumen al final.
    """
    req_cols = ["rut_docente", "nombre_doc", "apellidos_doc", "username_doc", "mail_doc"]
    faltantes = [c for c in req_cols if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el DataFrame: {faltantes}")

    # Trabajar solo con las 5 columnas esperadas y limpiar/normalizar valores
    base = df[req_cols].copy()
    base["rut_docente"]  = base["rut_docente"].map(_to_none_if_nan)              # clave
    base["nombre_doc"]   = base["nombre_doc"].map(_to_none_if_nan)
    base["apellidos_doc"]= base["apellidos_doc"].map(_to_none_if_nan)
    base["username_doc"] = base["username_doc"].map(lambda x: _to_none_if_nan(x, lower=True))
    base["mail_doc"]     = base["mail_doc"].map(lambda x: _to_none_if_nan(x, lower=True))

    # Detectar y contar duplicados por rut_docente en el origen (omitidos)
    dups_mask = base.duplicated(subset=["rut_docente"], keep="last")
    omitidos = int(dups_mask.sum())
    # Eliminar duplicados dejando el último
    work = base.drop_duplicates(subset=["rut_docente"], keep="last")

    mensaje_separador = "-------------------------------------------------------------"
    print(mensaje_separador)
    mensajes.append(mensaje_separador)

    fecha_hora_inicial = datetime.datetime.now()
    mensajes.append(
        f"Inicio del proceso de actualización: tabla {tabla_nombre.upper()}, {fecha_hora_inicial:%Y-%m-%d %H:%M:%S}"
    )
    print(mensajes[-1])

    conn = hace_conexion()

    nuevos = 0
    actualizados = 0
    ignorados = 0   # sin cambios
    errores = 0
    errores_detalle = []

    # IMPORTANTE: asume que existe UNIQUE(rut_docente).
    # Si no existe, crea: ALTER TABLE {tabla_nombre} ADD CONSTRAINT {tabla_nombre}_rut_docente_key UNIQUE (rut_docente);

    insert_sql = f"""
        INSERT INTO {tabla_nombre} (rut_docente, nombre_doc, apellidos_doc, username_doc, mail_doc)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (rut_docente) DO NOTHING
        RETURNING 1;
    """

    update_sql = f"""
        WITH datos(rut_docente, nombre_doc, apellidos_doc, username_doc, mail_doc) AS (
            VALUES (%s, %s, %s, %s, %s)
        )
        UPDATE {tabla_nombre} t
        SET
            nombre_doc    = d.nombre_doc,
            apellidos_doc = d.apellidos_doc,
            username_doc  = d.username_doc,
            mail_doc      = d.mail_doc
        FROM datos d
        WHERE t.rut_docente = d.rut_docente
          AND (
                t.nombre_doc    IS DISTINCT FROM d.nombre_doc OR
                t.apellidos_doc IS DISTINCT FROM d.apellidos_doc OR
                t.username_doc  IS DISTINCT FROM d.username_doc OR
                t.mail_doc      IS DISTINCT FROM d.mail_doc
              )
        RETURNING 1;
    """

    try:
        total_registros = len(work)
        with tqdm(total=total_registros, desc="Docentes") as pbar:
            cur = conn.cursor()
            for idx, row in work.iterrows():
                params = (
                    row["rut_docente"], row["nombre_doc"], row["apellidos_doc"],
                    row["username_doc"], row["mail_doc"]
                )

                try:
                    # 1) Intento de INSERT (si no existe -> nuevo)
                    cur.execute(insert_sql, params)
                    ins = cur.fetchone()
                    if ins:
                        nuevos += 1
                    else:
                        # 2) Intento de UPDATE (si cambió algo -> actualizado)
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
                    errores_detalle.append({
                        "idx": idx,
                        "rut_docente": row["rut_docente"],
                        "error": str(e)
                    })

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
            # Muestra hasta 10 errores para depurar
            muestras = errores_detalle[:10]
            mensajes.append(f"Ejemplos de errores (máx. 10): {muestras}")

    except Exception as e:
        mensajes.append(f"Error general: {e}")
        print(mensajes[-1])
    finally:
        cierra_conexion(conn)

    fecha_hora_final = datetime.datetime.now()
    mensajes.append(f"Finaliza el proceso: {fecha_hora_final:%Y-%m-%d %H:%M:%S}")
    mensajes.append(f"Tiempo utilizado: {round((fecha_hora_final - fecha_hora_inicial).total_seconds() / 60, 2)} minutos")
    mensajes.append(mensaje_separador)

    return mensajes
