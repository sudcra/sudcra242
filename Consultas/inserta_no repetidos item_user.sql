INSERT INTO matricula_eval_itemresp2
SELECT * FROM matricula_eval_itemresp_aux2
WHERE NOT EXISTS (
    SELECT 1
    FROM matricula_eval_itemresp
    WHERE matricula_eval_itemresp.id_mei = matricula_eval_itemresp_aux2.id_mei
);