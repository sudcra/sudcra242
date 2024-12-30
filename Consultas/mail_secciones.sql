select 
informes_secciones.id_eval,
informes_secciones.id_seccion,
docentes.nombre_doc || ' ' || docentes.apellidos_doc as docente,
docentes.mail_doc,
eval.nombre_prueba,
informes_secciones.id_eval || '_' || informes_secciones.id_seccion || '.html' as informe,
secciones.seccion,
asignaturas.programa

from informes_secciones
join 
eval on informes_secciones.id_eval=eval.id_eval
join 
secciones on secciones.id_seccion =informes_secciones.id_seccion
join
docentes on secciones.rut_docente = docentes.rut_docente
join
asignaturas on asignaturas.cod_asig = secciones.cod_asig