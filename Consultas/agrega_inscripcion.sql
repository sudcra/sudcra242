delete from inscripcion 
where id_inscripcion in (select inscripcion.id_inscripcion

from inscripcion

join secciones on secciones.id_seccion = inscripcion.id_seccion
join inscripcion_asig_a on inscripcion_asig_a.cod_asig = secciones.cod_asig and inscripcion_asig_a.id_matricula = inscripcion.id_matricula);

insert into inscripcion 
select * from inscripcion_a;