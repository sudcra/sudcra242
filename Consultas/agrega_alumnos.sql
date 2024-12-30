INSERT INTO alumnos
select * from alumnos_a
where rut not in (select rut  from alumnos)