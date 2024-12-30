SELECT
	listado_alumnos_pendientes.programa,
	listado_alumnos_pendientes.asig,
	listado_alumnos_pendientes.nombre_prueba,
	listado_alumnos_pendientes.num_prueba,
	calificaciones_obtenidas.lectura_fecha,
	listado_alumnos_pendientes.seccion,
	listado_alumnos_pendientes.nombre_doc || ' ' || listado_alumnos_pendientes.apellidos_doc as docente,
	case when
		condicion is null
		then False
		else True
	END as rinde	,
	listado_alumnos_pendientes.tiene_formas,
	listado_alumnos_pendientes.tiene_grupo,
	case when
		matricula_eval.imagen != ''
		then True
		else False
	END as tiene_imagen	,
	case when
		matricula_eval.imagen != ''
		then False
		else True
	END as tiene_planilla,
	case when
		calificaciones_obtenidas.logro_obtenido is null
		then False
		else True
	END as tiene_informe	,
	ROW_NUMBER() OVER () AS n,
	listado_alumnos_pendientes.rut,
	listado_alumnos_pendientes.apellidos || ' ' || listado_alumnos_pendientes.nombres as nombre_alum,
	matricula_eval.forma,
	matricula_eval.grupo,
	calificaciones.nota,
	calificaciones_obtenidas.logro_obtenido,
	calificaciones.condicion,
	case when
		matricula_eval.imagen != ''
		then 'https://duoccl0.sharepoint.com/sites/SUDCRA2/Lists/imgenes20242/Attachments/' || (string_to_array(matricula_eval.imagen, '_'))[1] || '/' || RIGHT(matricula_eval.imagen, LENGTH(matricula_eval.imagen) - LENGTH((string_to_array(matricula_eval.imagen, '_'))[1])-1)
		else ''
	END as imagen,
	 
    listado_alumnos_pendientes.id_seccion,
    listado_alumnos_pendientes.id_matricula,
    listado_alumnos_pendientes.id_eval,
    listado_alumnos_pendientes.id_matricula_eval,
    listado_alumnos_pendientes.nombre_sede,
    listado_alumnos_pendientes.rut_docente,
    listado_alumnos_pendientes.user_alum,
	eval_tipos_item.tipo_sm,
	eval_tipos_item.tipo_de,
	eval_tipos_item.tipo_ru,
    calificaciones_obtenidas.puntaje_total_obtenido,
	eval_tipos_item.total_puntos,
   	calificaciones_obtenidas.informe_listo,
    calificaciones.mensaje,
	listado_alumnos_pendientes.username_doc,
	eval.ver_correctas
FROM
    listado_alumnos_pendientes
	
JOIN eval_tipos_item on listado_alumnos_pendientes.id_eval = eval_tipos_item.id_eval
JOIN eval on listado_alumnos_pendientes.id_eval = eval.id_eval

LEFT JOIN
    calificaciones_obtenidas
ON
    listado_alumnos_pendientes.id_matricula_eval = calificaciones_obtenidas.id_matricula_eval
LEFT JOIN
    calificaciones
ON
    calificaciones_obtenidas.id_calificacion = calificaciones.id_calificacion
LEFT JOIN
    matricula_eval
ON
    listado_alumnos_pendientes.id_matricula_eval = matricula_eval.id_matricula_eval
LEFT JOIN
    imagenes
ON
    matricula_eval.imagen = imagenes.id_imagen


WHERE
    listado_alumnos_pendientes.id_seccion = [id_seccion]
    AND listado_alumnos_pendientes.id_eval = '[id_eval]'
order by listado_alumnos_pendientes.apellidos;