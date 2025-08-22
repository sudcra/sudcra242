import datetime
from eval_insert import hace_conexion, cierra_conexion
from psycopg2.extras import execute_values

def sync_inscripcion(df, mensajes):
    """
    Sincroniza 'inscripcion' contra el snapshot entregado (df) cargado en 'inscripcion_a'.
    Clave: id_inscripcion (puede haber múltiples por alumno).
    df debe incluir columnas: id_inscripcion, id_matricula, id_seccion, marca_temporal
    Reglas:
      - Los id_inscripcion presentes en df -> vigente=true (insert o update).
      - Los que están vigentes en 'inscripcion' y NO vienen en df -> vigente=false (soft delete).
      - Si df viene vacío, NO desactiva nada (protección como en matrícula).
    """
    sep = "-------------------------------------------------------------"
    print(sep); mensajes.append(sep)

    t0 = datetime.datetime.now()
    mensajes.append(f"Inicio sync INSCRIPCIÓN por id_inscripcion: {t0:%Y-%m-%d %H:%M:%S}")
    print(mensajes[-1])

    conn = hace_conexion()
    cur = conn.cursor()

    try:
        # 1) Limpiar staging y cargar snapshot (forzando vigente=TRUE en staging)
        cur.execute("TRUNCATE TABLE inscripcion_a;")

        cols = ["id_inscripcion","id_matricula","id_seccion","marca_temporal"]
        missing = [c for c in cols if c not in df.columns]
        if missing:
            raise ValueError(f"Faltan columnas en df: {missing}")

        rows = list(df[cols].itertuples(index=False, name=None))
        if rows:
            execute_values(
                cur,
                """
                INSERT INTO inscripcion_a (id_inscripcion, id_matricula, id_seccion, marca_temporal, vigente)
                VALUES %s
                """,
                rows,
                page_size=10000,
                template="(%s,%s,%s,%s, TRUE)"
            )

        # 2) Upsert + 3) Desactivar ausentes (solo si hay snapshot)
        cur.execute("""
        WITH snapshot_present AS (
          SELECT (COUNT(*) > 0) AS has_data FROM inscripcion_a
        ),
        upsert AS (
          INSERT INTO inscripcion (id_inscripcion, id_matricula, id_seccion, marca_temporal, vigente)
          SELECT a.id_inscripcion, a.id_matricula, a.id_seccion, a.marca_temporal, TRUE
          FROM inscripcion_a a
          ON CONFLICT (id_inscripcion) DO UPDATE
          SET id_matricula    = EXCLUDED.id_matricula,
              id_seccion      = EXCLUDED.id_seccion,
              marca_temporal  = EXCLUDED.marca_temporal,
              vigente         = TRUE
          WHERE inscripcion.id_matricula   IS DISTINCT FROM EXCLUDED.id_matricula
             OR inscripcion.id_seccion     IS DISTINCT FROM EXCLUDED.id_seccion
             OR inscripcion.marca_temporal IS DISTINCT FROM EXCLUDED.marca_temporal
             OR inscripcion.vigente        IS DISTINCT FROM TRUE
          RETURNING (xmax = 0)::int AS inserted, (xmax <> 0)::int AS updated
        ),
        counts AS (
          SELECT
            (SELECT COUNT(*) FROM inscripcion_a) AS total_snapshot,
            COALESCE(SUM(inserted),0)           AS inserted,
            COALESCE(SUM(updated),0)            AS updated
          FROM upsert
        ),
        deact AS (
          UPDATE inscripcion i
             SET vigente = FALSE,
                 marca_temporal = NOW()
            WHERE i.vigente = TRUE
              AND EXISTS (SELECT 1 FROM snapshot_present sp WHERE sp.has_data)
              AND NOT EXISTS (
                    SELECT 1 FROM inscripcion_a a
                    WHERE a.id_inscripcion = i.id_inscripcion
              )
          RETURNING 1
        )
        SELECT
          c.inserted                                         AS nuevos,
          c.updated                                          AS actualizados,
          GREATEST(c.total_snapshot - c.inserted - c.updated, 0) AS sin_cambios,
          (SELECT COUNT(*) FROM deact)                       AS desactivados
        FROM counts c;
        """)

        nuevos, actualizados, sin_cambios, desactivados = cur.fetchone()
        conn.commit()

        mensajes.append(
            f"Nuevos: {nuevos}, Actualizados: {actualizados}, Sin cambios: {sin_cambios}"
        )
        print(mensajes[-1])

    except Exception as e:
        conn.rollback()
        mensajes.append(f"Error en sync inscripcion (id_inscripcion): {e}")
        print(mensajes[-1])
        raise
    finally:
        cur.close()
        cierra_conexion(conn)

    t1 = datetime.datetime.now()
    mensajes.append(f"Fin sync: {t1:%Y-%m-%d %H:%M:%S}")
    mensajes.append(f"Tiempo: {round((t1 - t0).total_seconds()/60, 2)} min")
    mensajes.append(sep)
    print(mensajes[-1])

    return {
        "nuevos": nuevos,
        "actualizados": actualizados,
        "sin_cambios": sin_cambios,
        "desactivados": desactivados
    }
