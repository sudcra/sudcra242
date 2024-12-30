SELECT i.id_seccion,
    e.id_eval,
    e.num_prueba,
    e.retro_alum,
    e.retro_doc,
    e.exigencia,
    e.num_ppt
   FROM calificaciones_obtenidas co
     JOIN matricula_eval me ON co.id_matricula_eval::text = me.id_matricula_eval::text
     JOIN eval e ON me.id_eval::text = e.id_eval::text
     JOIN inscripcion i ON i.id_matricula::text = me.id_matricula::text
     JOIN secciones s ON s.id_seccion = i.id_seccion AND s.cod_asig::text = e.cod_asig::text
  WHERE i.id_seccion = [id_seccion] and e.id_eval= '[id_eval]'
  GROUP BY i.id_seccion, e.id_eval, e.num_prueba, e.retro_alum, e.retro_doc, e.exigencia, e.num_ppt;