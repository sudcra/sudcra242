insert into lectura_temp (rut,id_itemresp,id_archivoleido,linea_leida,reproceso,imagen,instante_forms,num_prueba,forma,grupo,cod_interno,registro_leido)
select l.rut
,l.id_itemresp
,l.id_archivoleido
,l.linea_leida
,true  as reproceso
,l.imagen
,l.instante_forms
,l.num_prueba
,l.forma
,l.grupo
,l.cod_interno
,l.registro_leido

from listado_temp lt
join matricula_eval me on me.id_matricula_eval = lt.id_matricula_eval 
join matricula mt on mt.id_matricula = me.id_matricula
join lectura l on l.rut = mt.rut and me.id_archivoleido = l.id_archivoleido