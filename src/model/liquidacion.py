# Auxilio de transporte (valor aproximado en COP para 2025)
AUX_TRANSPORTE = 162_000

# Porcentajes de deducciones al empleado
PORC_SALUD = 0.04
PORC_PENSION = 0.04

# Porcentajes de aportes del empleador
PORC_SALUD_EMP = 0.085
PORC_PENSION_EMP = 0.12
PORC_ARL = 0.0052
PORC_CAJA_COMPENSACION = 0.04
PORC_ICBF = 0.03
PORC_SENA = 0.02

# Recargos por horas extra
RECARGO_EXTRA_DIURNA = 1.25
RECARGO_EXTRA_NOCTURNA = 1.75
RECARGO_EXTRA_DOMINICAL = 2.0

# Provisiones
PORC_INTERESES_CESANTIAS = 0.12
DIVISOR_CESANTIAS = 360
DIVISOR_PRIMA = 360
DIVISOR_VACACIONES = 720


def calcular_valor_hora(salario_mensual: float) -> float:
    """Calcula el valor de una hora ordinaria a partir del salario mensual."""
    return salario_mensual / 30 / 8


def calcular_neto_a_pagar(
    salario_mensual: float,
    dias_trabajados: int,
    horas_extra_diurnas: int,
    horas_extra_nocturnas: int,
    horas_extra_dominicales: int,
    aplica_auxilio_transporte: bool
) -> float:
    """Calcula el salario neto a pagar al empleado."""

    valor_hora: float = calcular_valor_hora(salario_mensual)

    pago_extra_diurna: float = horas_extra_diurnas * valor_hora * RECARGO_EXTRA_DIURNA
    pago_extra_nocturna: float = horas_extra_nocturnas * valor_hora * RECARGO_EXTRA_NOCTURNA
    pago_extra_dominical: float = horas_extra_dominicales * valor_hora * RECARGO_EXTRA_DOMINICAL

    salario_base: float = salario_mensual * dias_trabajados / 30
    auxilio_transporte: float = AUX_TRANSPORTE if aplica_auxilio_transporte else 0

    total_ingresos: float = (
        salario_base
        + auxilio_transporte
        + pago_extra_diurna
        + pago_extra_nocturna
        + pago_extra_dominical
    )

    descuento_salud: float = salario_base * PORC_SALUD
    descuento_pension: float = salario_base * PORC_PENSION
    total_deducciones: float = descuento_salud + descuento_pension

    return total_ingresos - total_deducciones


def calcular_provisiones(salario_mensual: float, dias_trabajados: int) -> float:
    """Calcula provisiones de prestaciones sociales (cesantías, intereses, prima, vacaciones)."""
    cesantias: float = salario_mensual * dias_trabajados / DIVISOR_CESANTIAS
    intereses_cesantias: float = cesantias * PORC_INTERESES_CESANTIAS
    prima: float = salario_mensual * dias_trabajados / DIVISOR_PRIMA
    vacaciones: float = salario_mensual * dias_trabajados / DIVISOR_VACACIONES

    return cesantias + intereses_cesantias + prima + vacaciones


def calcular_aportes_empleador(salario_mensual: float) -> float:
    """Calcula el total de aportes a seguridad social y parafiscales a cargo del empleador."""
    aporte_salud: float = salario_mensual * PORC_SALUD_EMP
    aporte_pension: float = salario_mensual * PORC_PENSION_EMP
    aporte_arl: float = salario_mensual * PORC_ARL
    aporte_caja_compensacion: float = salario_mensual * PORC_CAJA_COMPENSACION
    aporte_icbf: float = salario_mensual * PORC_ICBF
    aporte_sena: float = salario_mensual * PORC_SENA

    return (
        aporte_salud
        + aporte_pension
        + aporte_arl
        + aporte_caja_compensacion
        + aporte_icbf
        + aporte_sena
    )
