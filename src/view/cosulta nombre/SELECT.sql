SELECT 
       nombre,
       salario_mensual,
       dias_trabajados,
       horas_extras_diurnas,
       horas_extras_nocturnas,
       horas_extras_dominicales,
       aplica_auxilio_transporte
FROM public.liquidacion_nomina
empleados WHERE nombre ilike 'juan %'; -- consultar por abrebiaturas 





