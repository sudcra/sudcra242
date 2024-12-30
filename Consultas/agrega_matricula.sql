insert into matricula 
select matricula_a.id_matricula,
matricula_a.rut,
matricula_a.id_sede,
matricula_a.cod_plan,
2024 as ano,
1 as periodo

from matricula_a
where matricula_a.id_matricula not in (select id_matricula from matricula)