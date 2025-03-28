-- Trigger para modificar campo num_prueba tabla EVAL
CREATE OR REPLACE FUNCTION update_eval_trigger()
RETURNS TRIGGER AS $$
DECLARE
    codinterno TEXT;
	nprueba TEXT;
BEGIN
    -- Obtener el cod_interno de la tabla asignaturas basado en cod_asig
    SELECT cod_interno INTO codinterno 
    FROM asignaturas 
    WHERE cod_asig = NEW.cod_asig;
    
    -- Asegurar que num_prueba tenga dos dígitos
    nprueba := LPAD(NEW.num_prueba::TEXT, 2, '0');

    -- Concatenar cod_interno con num_prueba y almacenarlo en num_prueba
    NEW.num_prueba := codinterno || nprueba;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_eval
BEFORE INSERT ON eval
FOR EACH ROW
EXECUTE FUNCTION update_eval_trigger();

-- Trigger para eliminar registro en tabla MEDIDAS al eliminar registro en tabla EVAL
-- Primero elimina los registros asociados a id_medida de la tabla relacionada ITEM_MEDIDA
CREATE OR REPLACE FUNCTION eliminar_medidas_relacionadas()
RETURNS TRIGGER AS $$
BEGIN
    -- 1️⃣ Eliminar registros en item_medida que dependan de medidas
    DELETE FROM item_medida 
    WHERE id_medida IN (SELECT id_medida FROM medidas WHERE id_eval = OLD.id_eval);

    -- 2️⃣ Ahora que no hay dependencias, eliminar los registros en medidas
    DELETE FROM medidas WHERE id_eval = OLD.id_eval;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_eliminar_medidas
AFTER DELETE ON eval
FOR EACH ROW
EXECUTE FUNCTION eliminar_medidas_relacionadas();

