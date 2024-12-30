select 
s.id_seccion,
asig.cod_programa,
sd.cod_sede,
s.cod_asig,
s.seccion
from secciones s
join asignaturas asig on asig.cod_asig = s.cod_asig
join sedes sd on sd.id_sede = s.id_sede
join inscripcion i on i.id_seccion = s.id_seccion
where s.cod_asig = '[cod_asig]' 
[seccion]
group by
s.id_seccion,
asig.cod_programa,
sd.cod_sede,
s.cod_asig,
s.seccion