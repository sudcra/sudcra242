select	 i.id_item
		,i.forma
		,i.item_orden
		,i.item_tipo
		,i.item_num
		,i.item_nombre
		,ir.registro
		,i.item_puntaje
		,ir.puntaje_asignado

from item i 
join eval e on e.id_eval = i.id_eval
join item_respuesta ir on ir.id_item = i.id_item
where e.cod_asig = '[cod_asig]' and e.num_prueba = [num_prueba];