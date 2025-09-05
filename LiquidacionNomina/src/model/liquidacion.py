# Valores fijos
AUX_TRANSPORTE = 162000  # Valor 2025 aprox
PORC_SALUD = 0.04
PORC_PENSION = 0.04

PORC_SALUD_EMP = 0.085
PORC_PENSION_EMP = 0.12
PORC_ARL = 0.0052
PORC_CAJA = 0.04
PORC_ICBF = 0.03
PORC_SENA = 0.02

def calcular_valor_hora(salario):
    return salario / 30 / 8

def calcular_neto_a_pagar(salario, dias, h_extra_d, h_extra_n, h_extra_dom, aplica_aux):
    valor_hora = calcular_valor_hora(salario)

    # Horas extra
    extra_d = h_extra_d * valor_hora * 1.25
    extra_n = h_extra_n * valor_hora * 1.75
    extra_dom = h_extra_dom * valor_hora * 2

    # Salario proporcional a días trabajados
    salario_base = salario * dias / 30

    # Auxilio transporte
    aux = AUX_TRANSPORTE if aplica_aux else 0

    # Ingresos
    total_ingresos = salario_base + aux + extra_d + extra_n + extra_dom

    # Deducciones
    salud = salario_base * PORC_SALUD
    pension = salario_base * PORC_PENSION

    deducciones = salud + pension

    return total_ingresos - deducciones

def calcular_provisiones(salario, dias):
    # Cesantías, intereses, prima y vacaciones
    cesantias = salario * dias / 360
    intereses = cesantias * 0.12
    prima = salario * dias / 360
    vacaciones = salario * dias / 720
    return cesantias + intereses + prima + vacaciones

def calcular_aportes_empleador(salario):
    salud = salario * PORC_SALUD_EMP
    pension = salario * PORC_PENSION_EMP
    arl = salario * PORC_ARL
    caja = salario * PORC_CAJA
    icbf = salario * PORC_ICBF
    sena = salario * PORC_SENA
    return salud + pension + arl + caja + icbf + sena
