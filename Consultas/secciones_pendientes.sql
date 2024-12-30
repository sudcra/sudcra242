select 
i.id_seccion,
e.id_eval,
e.num_prueba,
e.retro_alum,
e.retro_doc,
e.exigencia,
e.num_ppt
from
calificaciones_obtenidas as co
join matricula_eval as me on co.id_matricula_eval = me.id_matricula_eval
join eval as e  on me.id_eval = e.id_eval
join inscripcion as i on i.id_matricula = me.id_matricula
join secciones as s on s.id_seccion = i.id_seccion and s.cod_asig = e.cod_asig
where 
co.informe_listo = false
group by 
i.id_seccion,
e.id_eval,
e.num_prueba,
e.retro_alum,
e.retro_doc,
e.exigencia,
e.num_ppt