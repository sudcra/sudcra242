update secciones
set rut_docente = secciones_a.rut_docente
from secciones_a
where
secciones.id_seccion = secciones_a.id_seccion