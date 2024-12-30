update errores
set valida_inscripcion = true

from actualiza_errores_inscripcion
where errores.id_error = actualiza_errores_inscripcion.id_error;