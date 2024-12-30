update errores
set id_seccion = secciones.id_seccion
from secciones 
where
secciones.id_sede = cast(SPLIT_PART(imagen,'_',2) as integer) and secciones.seccion = SPLIT_PART(imagen,'_',3) and errores.id_seccion is NULL
;