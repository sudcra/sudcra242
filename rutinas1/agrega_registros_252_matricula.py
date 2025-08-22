import datetime
from eval_insert import hace_conexion, cierra_conexion
from psycopg2.extras import execute_values

def sync_matricula(df, mensajes):
    sep = "-------------------------------------------------------------"
    print(sep); mensajes.append(sep)

    t0 = datetime.datetime.now()
    mensajes.append(f"Inicio sync MATRÍCULA por id_matricula: {t0:%Y-%m-%d %H:%M:%S}")
    print(mensajes[-1])

    conn = hace_conexion()
    cur = conn.cursor()

    try:
        cur.execute("TRUNCATE TABLE matricula_a;")

        cols = ["id_matricula","rut","id_sede","cod_plan","ano","periodo","marca_temporal","estado"]
        missing = [c for c in cols if c not in df.columns]
        if missing:
            raise ValueError(f"Faltan columnas en df: {missing}")

        rows = list(df[cols].itertuples(index=False, name=None))
        if rows:
            execute_values(
                cur,
                """
                INSERT INTO matricula_a (id_matricula, rut, id_sede, cod_plan, ano, periodo, marca_temporal, estado)
                VALUES %s
                """,
                rows,
                page_size=10000
            )

        cur.execute("""
        WITH scope AS (
          SELECT DISTINCT ano, periodo FROM matricula_a
        ),
        upsert AS (
          INSERT INTO matricula (id_matricula, rut, id_sede, cod_plan, ano, periodo, marca_temporal, vigente, estado)
          SELECT a.id_matricula, a.rut, a.id_sede, a.cod_plan, a.ano, a.periodo, a.marca_temporal, TRUE, a.estado
          FROM matricula_a a
          ON CONFLICT (id_matricula) DO UPDATE
          SET rut            = EXCLUDED.rut,
              id_sede        = EXCLUDED.id_sede,
              cod_plan       = EXCLUDED.cod_plan,
              ano            = EXCLUDED.ano,
              periodo        = EXCLUDED.periodo,
              marca_temporal = EXCLUDED.marca_temporal,
              vigente        = TRUE,
              estado         = EXCLUDED.estado
          WHERE matricula.rut            IS DISTINCT FROM EXCLUDED.rut
             OR matricula.id_sede        IS DISTINCT FROM EXCLUDED.id_sede
             OR matricula.cod_plan       IS DISTINCT FROM EXCLUDED.cod_plan
             OR matricula.ano            IS DISTINCT FROM EXCLUDED.ano
             OR matricula.periodo        IS DISTINCT FROM EXCLUDED.periodo
             OR matricula.marca_temporal IS DISTINCT FROM EXCLUDED.marca_temporal
             OR matricula.vigente        IS DISTINCT FROM TRUE
             OR matricula.estado         IS DISTINCT FROM EXCLUDED.estado
          RETURNING (xmax = 0)::int AS inserted, (xmax <> 0)::int AS updated
        ),
        counts AS (
          SELECT
            (SELECT COUNT(*) FROM matricula_a) AS total_snapshot,
            COALESCE(SUM(inserted),0)         AS inserted,
            COALESCE(SUM(updated),0)          AS updated
          FROM upsert
        ),
        deact AS (
          UPDATE matricula m
             SET vigente = FALSE,
                 marca_temporal = NOW()
            WHERE m.vigente = TRUE
              AND EXISTS (SELECT 1 FROM scope s WHERE s.ano = m.ano AND s.periodo = m.periodo)
              AND NOT EXISTS (
                    SELECT 1 FROM matricula_a a
                    WHERE a.id_matricula = m.id_matricula
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
        mensajes.append(f"Error en sync matricula (id_matricula): {e}")
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
