SELECT * FROM public.lectura_avatemp

delete from lectura_avatemp

select * from matricula

select * from item where item_tipo = 'DE'
select * from lectura where id_itemresp ='2024002MAT31100102012'
select * from item_respuesta where id_itemresp ='2024002701150051'

select 
al.rut,
CASE WHEN item.item_tipo = 'DE' then
  ano || '00' || periodo || la.id_item
ELSE
	CASE WHEN respuesta <> '<Sin contesta' AND (registroa + registrom) = 0 then
		ano || '00' || periodo || la.id_item || '2'
	ELSE	
  		ano || '00' || periodo || la.id_item || CAST(GREATEST(registroa , registrom) AS INT)
	END	
END as id_itemresp,
id_archivoleido,
linea_leida,
case when rep = 'R' then
 true
else
 false
end as reproceso,
CURRENT_TIMESTAMP as instante_forms,
CAST(left(right(la.id_item,7),2) as INT) as num_prueba,
CAST(left(right(la.id_item,5),2) as INT) as forma,
1 as grupo,
asig.cod_interno,
CASE WHEN item.item_tipo = 'DE' then
  CAST(registroa + registrom AS INT)
ELSE
 	CASE WHEN respuesta <> '<Sin contesta' AND (registroa + registrom) = 0 then
		2
	ELSE	
  		CAST(GREATEST(registroa , registrom) AS INT)
	END	
END as registro_leido
from lectura_avatemp la
join alumnos al on la.user_alum = al.user_alum
join matricula mt on al.rut =mt.rut
JOIN asignaturas asig on asig.cod_interno = CASE WHEN LENGTH(la.id_item)>7 THEN
substring(la.id_item, 1,LENGTH(la.id_item)-7) 
ELSE
NULL
END
join item on item.id_item = ano || '00' || periodo || cod_asig || right(la.id_item,7)
order by linea_leida