insert into docentes
select * from docentes_a
where rut_docente not in (select docentes.rut_docente from docentes)