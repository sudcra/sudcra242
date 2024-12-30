SELECT 

MATE.id_eval,
S.id_seccion,
MATE.id_matricula_eval,
I.item_tipo,
I.item_num,
I.item_nombre,
IR.registro,
IR.puntaje_asignado,
I.item_puntaje,
E.nivel,
E.nivel_descripcion
	
from secciones as S
join inscripcion as INS on INS.id_seccion = S.id_seccion
join matricula as MAT on MAT.id_matricula = INS.id_matricula
join matricula_eval as MATE on MAT.id_matricula = MATE.id_matricula
join item as I on I.id_eval = MATE.id_eval
join item_respuesta as IR on I.id_item = IR.id_item
join escala as E on E.id_eval =  MATE.id_eval and E.cod_nivel=IR.registro
join matricula_eval_itemresp as IRA on IRA.id_itemresp = IR.id_itemresp and IRA.id_matricula_eval = MATE.id_matricula_eval
WHERE I.item_tipo='RU' and S.id_seccion=[id_seccion] and MATE.id_eval = '[id_eval]' 
ORDER BY 
    MATE.id_matricula_eval, 
    I.item_orden;