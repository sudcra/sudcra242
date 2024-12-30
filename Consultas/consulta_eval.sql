select 	e.id_eval
		,e.cod_asig
		,e.ano
		,e.periodo
		,e.num_prueba
		,e.nombre_prueba
		,e.tiene_formas
		,e.retro_alum
		,e.retro_doc
		,e.ver_correctas
		,e.tiene_grupo
		,e.archivo_tabla
		,e.cargado_fecha
		,e.exigencia
		,e.num_ppt
		,asig.cod_interno
		,'proceso202402' as validap
		from eval e
		join asignaturas asig on asig.cod_asig = e.cod_asig
		where e.cod_asig = '[cod_asig]' and e.num_prueba = [num_prueba];
		
		