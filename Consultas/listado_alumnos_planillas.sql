select 
al.apellidos || ' ' || al.nombres as alumno,
al.rut
from secciones s
join inscripcion i on i.id_seccion = s.id_seccion
join matricula mt on mt.id_matricula=i.id_matricula
join alumnos al on al.rut = mt.rut
where s.id_seccion = [id_seccion]
order by al.apellidos