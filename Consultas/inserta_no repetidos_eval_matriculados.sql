INSERT INTO matricula_eval 
select * from matricula_eval_aux
where id_matricula_eval not in (select id_matricula_eval from matricula_eval);

