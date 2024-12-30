select 
	id_seccion,
	id_eval,
	orden,
	id_medida,
	nombre_tipo_medida,
	desc_larga,
	logro,
	nombre_tipo_medida2,
	desc_larga2,
	logro2
	from (SELECT 
	inscripcion.id_seccion, 
	matricula_eval.id_eval, 
	medidas.orden, 
	medidas.id_medida, 
	medidas.desc_larga, 
	Sum(matricula_eval_itemresp.puntaje_alum)/Sum(item.item_puntaje) AS logro, 
	medidas.url_retro, 
	medidas.dependencia,
	medidas.tipo_medida_cod,
	tipo_medida.nombre_tipo_medida  
FROM inscripcion 
	JOIN 
	matricula_eval ON matricula_eval.id_matricula = inscripcion.id_matricula
	JOIN 
	matricula_eval_itemresp ON matricula_eval_itemresp.id_matricula_eval = matricula_eval.id_matricula_eval
	JOIN 
	item_respuesta ON item_respuesta.id_itemresp = matricula_eval_itemresp.id_itemresp
	JOIN 
	item ON item.id_item = item_respuesta.id_item
	JOIN 
	item_medida ON item_medida.id_item = item.id_item
	JOIN
	medidas ON medidas.id_medida = item_medida.id_medida
	JOIN
	tipo_medida ON medidas.tipo_medida_cod = tipo_medida.tipo_medida_cod
GROUP BY 
	inscripcion.id_seccion , 
	matricula_eval.id_eval ,
	medidas.orden , 
	medidas.id_medida , 
	medidas.desc_larga  ,
	medidas.url_retro ,
	medidas.dependencia,
	tipo_medida.tipo_medida_cod	  
HAVING 
	inscripcion.id_seccion=[id_seccion] AND 
	matricula_eval.id_eval='[id_eval]')  as medidas_seccion
	
join
  (SELECT 
	inscripcion.id_seccion as id_seccion2, 
	matricula_eval.id_eval as id_eval2 , 
	medidas.orden as orden2, 
	medidas.id_medida as id_medida2, 
	medidas.desc_larga as desc_larga2, 
	Sum(matricula_eval_itemresp.puntaje_alum)/Sum(item.item_puntaje) AS logro2, 
	medidas.url_retro as url_retro2, 
	medidas.dependencia as dependencia2,
	medidas.tipo_medida_cod as tipo,
    tipo_medida.nombre_tipo_medida  as nombre_tipo_medida2
FROM inscripcion 
	JOIN 
	matricula_eval ON matricula_eval.id_matricula = inscripcion.id_matricula
	JOIN 
	matricula_eval_itemresp ON matricula_eval_itemresp.id_matricula_eval = matricula_eval.id_matricula_eval
	JOIN 
	item_respuesta ON item_respuesta.id_itemresp = matricula_eval_itemresp.id_itemresp
	JOIN 
	item ON item.id_item = item_respuesta.id_item
	JOIN 
	item_medida ON item_medida.id_item = item.id_item
	JOIN
	medidas ON medidas.id_medida = item_medida.id_medida
	JOIN
	tipo_medida ON medidas.tipo_medida_cod = tipo_medida.tipo_medida_cod
GROUP BY 
	inscripcion.id_seccion, 
	matricula_eval.id_eval, 
	medidas.orden, 
	medidas.id_medida, 
	medidas.desc_larga, 
	medidas.url_retro, 
	medidas.dependencia,
	tipo_medida.tipo_medida_cod	  
HAVING 
	inscripcion.id_seccion=[id_seccion] AND 
	matricula_eval.id_eval='[id_eval]')as medidas_seccionil  on medidas_seccion.id_medida = medidas_seccionil.dependencia2
	
	where tipo_medida_cod='[medida]'
	order by orden, orden2
	;