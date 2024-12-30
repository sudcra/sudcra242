select id_itemresp,
registro,
puntaje_asignado
from item_respuesta
where id_item ='[id_item]' and registro != 0
order by registro;