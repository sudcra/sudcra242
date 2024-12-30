update lectura_avatemp set registrom = NULL
where registrom = 'NaN';
--parche error MAT4121 prueba 1********************************
--update lectura_avatemp set id_item = '510103006'
--where id_item = '93';
--parche error MAT4121 prueba 2********************************
--update lectura_avatemp set id_item = '510201004'
--where id_item = '';
--***********************************************************

INSERT INTO lectura_temp (rut,id_itemresp,id_archivoleido,linea_leida,reproceso,instante_forms,num_prueba,forma,grupo,cod_interno,registro_leido)
select 
al.rut,
CASE WHEN item.item_tipo = 'DE' then
  ano || '00' || periodo || la.id_item
ELSE
	CASE WHEN respuesta <> '<Sin contesta' AND registroa= 0  AND (registrom= 0 or registrom is NULL)  then
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
  case when registrom is NULL then
    registroa
  ELSE
  	registrom
  end	
ELSE
 	CASE WHEN respuesta <> '<Sin contesta' AND registroa= 0  AND (registrom= 0 or registrom is NULL) then
		2
	ELSE
		case when registrom is NULL then
    		CAST(registroa AS INT)
  		ELSE
  			CAST(registrom AS INT)
  		end	
  		
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
order by linea_leida;
delete from lectura_avatemp;