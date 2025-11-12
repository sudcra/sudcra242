from conecta_a_postgres import conectar_a_postgres

def eliminar_inscripciones_no_vigentes():
    """
    Elimina todos los registros de la tabla 'inscripcion'
    cuyo campo 'vigente' sea igual a false.
    """
    conexion = None
    cursor = None
    try:
        conexion = conectar_a_postgres()
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM inscripcion WHERE vigente = false;")
        conexion.commit()

        print("Se eliminaron todas las inscripciones con vigente = false.")

    except Exception as e:
        print(f"Error al eliminar inscripciones no vigentes: {e}")

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


# Permite ejecutar el módulo directamente desde la consola
if __name__ == "__main__":
    eliminar_inscripciones_no_vigentes()
