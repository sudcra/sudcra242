INSERT INTO errores (rut, num_prueba,cod_interno, forma, grupo, id_archivoleido, linea_leida, imagen, instante_forms)
SELECT leidos.rut, leidos.num_prueba, leidos.cod_interno, leidos.forma, leidos.grupo, leidos.id_archivoleido, leidos.linea_leida, leidos.imagen, leidos.instante_forms
FROM leidos
LEFT JOIN resultados ON leidos.imagen = resultados.imagen 
WHERE resultados.imagen IS NULL;