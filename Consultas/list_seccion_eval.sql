select --* 
	asig.programa
	,asig.asig
	,e.nombre_prueba
	,e.num_prueba
	,co.lectura_fecha
	,s.seccion
	,doc.nombre_doc || ' ' || doc.apellidos_doc as docente
	,case when
		condicion is null
		then False
		else True
	END as rinde
	,e.tiene_formas
	,e.tiene_grupo
	,case when
		im.url_imagen is null
		then False
		else True
	END as tiene_imagen	
	,case when
		im.url_imagen is null
		then True
		else False
	END as tiene_planilla
	,case when
		co.logro_obtenido is null
		then False
		else True
	END as tiene_informe
	,ROW_NUMBER() OVER () AS n
	,al.rut
	,al.apellidos || ' ' || al.nombres as nombre_alum
	,me.forma
	,me.grupo
	,ca.nota
	,co.logro_obtenido
	,ca.condicion
	,im.url_imagen as imagen
	,s.id_seccion
    ,mt.id_matricula
    ,me.id_eval
    ,me.id_matricula_eval
    ,sd.nombre_sede
    ,doc.rut_docente
    ,al.user_alum
	,eti.tipo_sm
	,eti.tipo_de
	,eti.tipo_ru
    ,co.puntaje_total_obtenido
	,eti.total_puntos
   	,co.informe_listo
    ,ca.mensaje
	,doc.username_doc
	,e.ver_correctas
from inscripcion  i
join secciones s on i.id_seccion = s.id_seccion
join sedes sd on sd.id_sede = s.id_sede
join docentes doc on doc.rut_docente = s.rut_docente
join asignaturas asig on asig.cod_asig = s.cod_asig
join matricula mt on mt.id_matricula = i.id_matricula
join alumnos al on al.rut = mt.rut

left join matricula_eval me on i.id_matricula = me.id_matricula and me.id_eval ='[id_eval]'
LEFT JOIN imagenes im ON me.imagen = im.id_imagen
left join eval e on e.id_eval = me.id_eval
left join eval_tipos_item eti on eti.id_eval = e.id_eval
left join calificaciones_obtenidas co on co.id_matricula_eval = me.id_matricula_eval
left join calificaciones ca on ca.id_calificacion = co.id_calificacion
where i.id_seccion = [id_seccion] 
order by al.apellidos