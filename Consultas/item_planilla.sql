select 
I.id_item,
I.item_orden,
I.item_nombre,
I.item_tipo,
I.item_puntaje

from item as I
where I.id_eval ='[id_eval]' and I.forma =1 ;