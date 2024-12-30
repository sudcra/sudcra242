DELETE FROM matricula_eval
WHERE id_matricula_eval IN (
    SELECT id_matricula_eval
    FROM reprocesos
);