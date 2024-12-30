update errores
set valida_eval = true

from actualiza_errores_eval
where errores.id_error = actualiza_errores_eval.id_error;