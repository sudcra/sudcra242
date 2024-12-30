INSERT INTO calificaciones_obtenidas (id_matricula_eval, puntaje_total_obtenido, logro_obtenido, num_prueba, convalida)
SELECT calificaciones_obtenidas_aux.id_matricula_eval, puntaje_total_obtenido, logro_obtenido, num_prueba, cod_convalida
FROM calificaciones_obtenidas_aux 
INNER JOIN
matricula_eval ON calificaciones_obtenidas_aux.id_matricula_eval = matricula_eval.id_matricula_eval
INNER JOIN
cantidad_item_eval ON cantidad_item_eval.id_eval = matricula_eval.id_eval
WHERE NOT EXISTS (
    SELECT 1
    FROM calificaciones_obtenidas
    WHERE calificaciones_obtenidas.id_matricula_eval = calificaciones_obtenidas_aux.id_matricula_eval 
)and cantidad_item_eval.count = calificaciones_obtenidas_aux.count;