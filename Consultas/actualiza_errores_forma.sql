update errores
set valida_forma = true

from actualiza_errores_forma
where errores.id_error = actualiza_errores_forma.id_error;