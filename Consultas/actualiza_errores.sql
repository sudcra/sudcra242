
update errores
set valida_rut = actualiza_errores.validadv,
valida_matricula = actualiza_errores.valida_matricula

from actualiza_errores
where errores.id_error = actualiza_errores.id_error;