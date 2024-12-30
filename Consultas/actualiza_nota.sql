UPDATE calificaciones_obtenidas
SET id_calificacion = calificaciones.id_calificacion, lectura_fecha= NOW()
FROM calificaciones
join matricula_eval on matricula_eval.id_eval = calificaciones.id_eval

WHERE calificaciones_obtenidas.id_calificacion is NULL AND
matricula_eval.id_matricula_eval =calificaciones_obtenidas.id_matricula_eval AND
case when num_prueba = 0 then

calificaciones_obtenidas.convalida=calificaciones.nota
else

calificaciones_obtenidas.puntaje_total_obtenido >= calificaciones.puntaje_inf AND calificaciones_obtenidas.puntaje_total_obtenido < calificaciones.puntaje_sup
end
;