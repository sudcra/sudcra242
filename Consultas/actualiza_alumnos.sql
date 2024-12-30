update alumnos
set user_alum = alumnos_a.user_alum
from alumnos_a
where alumnos.rut=alumnos_a.rut and alumnos.user_alum = ''