select 
docentes.nombre_doc || ' ' || docentes.apellidos_doc as docente,
docentes.mail_doc,
alumnos.nombres || ' ' || alumnos.apellidos as alumno,
alumnos.user_alum || '@DUOCUC.CL' AS mail_alum,
eval.nombre_prueba,
informe_alumnos.id_matricula_eval || '.html' as informe,
asignaturas.asig,
secciones.seccion,
sedes.nombre_sede as sede



from informe_alumnos
join
matricula_eval on matricula_eval.id_matricula_eval =informe_alumnos.id_matricula_eval 
join 
matricula on matricula.id_matricula = matricula_eval.id_matricula
join
alumnos on alumnos.rut =matricula.rut
join 
eval on eval.id_eval = matricula_eval.id_eval
join 
asignaturas on asignaturas.cod_asig = eval.cod_asig
join 
inscripcion on inscripcion.id_matricula = matricula.id_matricula
join 
secciones on secciones.id_seccion = inscripcion.id_seccion and secciones.cod_asig = eval.cod_asig
join 
docentes on secciones.rut_docente = docentes.rut_docente
join 
sedes on sedes.id_sede= secciones.id_sede
where informe_alumnos.mail_enviado = false 