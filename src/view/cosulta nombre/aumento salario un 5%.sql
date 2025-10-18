--borrar los trabajadores con menos de 5 dias tranajados 

DELETE FROM liquidacion_nomina
WHERE dias_trabajados < 5;

