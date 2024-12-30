 SELECT errores.id_error,
 	imagenes.docente,
    imagenes.mail,
    imagenes.evaluacion,
    ((imagenes.cod_asig::text || '-'::text) || lpad(imagenes.num_seccion::text, 3, '0'::text)) || imagenes.jornada::text AS seccion,
    imagenes.imagen,
    imagenes.url_imagen,
        CASE
            WHEN errores.rut IS NULL THEN 'No identificada'::text
            ELSE 'Leída'::text
        END AS eimag,
        CASE
            WHEN errores.rut IS NULL THEN '-'::character varying
            ELSE errores.rut
        END AS rut,
        CASE
            WHEN errores.valida_rut = true THEN
            CASE
                WHEN errores.valida_matricula = true THEN 'Válido'::text
                ELSE 'el rut leído no registra matrícula'::text
            END
            ELSE 'No válido'::text
        END AS erut,
		errores.cod_interno as asig_leida,
        CASE
            WHEN asignaturas.cod_asig IS NULL THEN '-'::character varying
            ELSE asignaturas.cod_asig
        END AS cod_asig,
        CASE
            WHEN asignaturas.cod_asig IS NULL THEN 'No se lee marca de asignatura'::text
            ELSE
            CASE
                WHEN errores.valida_inscripcion = true THEN 'Registro correcto'::text
                ELSE 'No se registra inscripción para la asignatura marcada'::text
            END
        END AS easig,
		errores.num_prueba as prueba_leida,
        CASE
            WHEN eval.nombre_prueba IS NULL THEN '-'::character varying
            ELSE eval.nombre_prueba
        END AS nombre_prueba,
        CASE
            WHEN errores.valida_eval = true THEN 'Evaluación identificada'::text
            ELSE 'No existe en sistema la evaluación registrada'::text
        END AS eprueba,
		
        CASE
            WHEN errores.forma IS NULL THEN '-'::text
            ELSE errores.forma::text
        END AS forma,
        CASE
            WHEN errores.forma = 0 THEN 'No se lee forma marcada'::text
            ELSE
            CASE
                WHEN errores.valida_forma = true THEN 'Forma identificada'::text
                ELSE 'No existe en sistema la forma registrada'::text
            END
        END AS eforma,
        CASE
            WHEN errores.valida_rut = true AND errores.valida_matricula = true AND errores.valida_inscripcion = true AND errores.valida_eval = true AND errores.valida_forma = true THEN 'que ya tiene informe enviado y no se ha registrado la marca de reproceso.'::text
            ELSE 'un error de lectura o de identificación.'::text
        END AS tipo
   FROM errores
     JOIN imagenes ON imagenes.id_imagen::text = errores.imagen::text
     LEFT JOIN asignaturas ON asignaturas.cod_interno::text = errores.cod_interno::text
     LEFT JOIN eval ON asignaturas.cod_asig::text = eval.cod_asig::text AND eval.num_prueba = errores.num_prueba
 