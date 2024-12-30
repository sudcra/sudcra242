update errores
set
valida_inscripcion = false
where valida_inscripcion is null;

update errores
set
valida_eval = false
where valida_eval is null;

update errores
set
valida_forma = false
where valida_forma is null;