select 	escala.id_escala 
		,escala.cod_nivel
		,escala.nivel
		,escala.nivel_descripcion
		,escala.id_eval
from escala 
join eval on eval.id_eval = escala.id_eval 
where eval.cod_asig = '[cod_asig]' and eval.num_prueba = [num_prueba];