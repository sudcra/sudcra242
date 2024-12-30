SELECT i.item_orden, i.item_tipo from item i
join eval e on e.id_eval = i.id_eval
join asignaturas asig on asig.cod_asig = e.cod_asig
where e.num_prueba = [prueba] and asig.cod_interno = '[asig]'