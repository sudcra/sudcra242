insert into secciones
select * from secciones_a
where id_seccion not in (select secciones.id_seccion from secciones)