SELECT 
I.item_orden,
SUM(MEI.puntaje_alum)/SUM(I.item_puntaje) AS logro
FROM secciones AS S
JOIN inscripcion AS INS ON INS.id_seccion = S.id_seccion
JOIN matricula AS MAT ON MAT.id_matricula = INS.id_matricula
JOIN matricula_eval AS ME ON MAT.id_matricula = ME.id_matricula
JOIN matricula_eval_itemresp AS MEI ON MEI.id_matricula_eval = ME.id_matricula_eval
JOIN item_respuesta AS IR ON IR.id_itemresp = MEI.id_itemresp
JOIN item AS I ON I.id_item = IR.id_item
WHERE
S.id_seccion = [id_seccion] and ME.id_eval = '[id_eval]'
GROUP BY
S.id_seccion,
I.item_orden
ORDER BY logro
LIMIT [n];