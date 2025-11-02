# --------------------------------------------
# src/model/liquidacion.py — Cálculos completos de nómina y liquidaciones
# --------------------------------------------
# --- bootstrap rutas ---
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# -----------------------

from src.database import get_connection

# --------------------------------------------
# 🔹 CONSTANTES GENERALES (valores aproximados en COP para 2025)
# --------------------------------------------

AUX_TRANSPORTE = 162_000  # Auxilio de transporte

# Porcentajes de deducciones del empleado
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


# --------------------------------------------
# 🔹 FUNCIONES DE CÁLCULO
# --------------------------------------------

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
    """
    Calcula el salario neto a pagar al empleado.
    Incluye salario base, horas extra, auxilio de transporte y descuentos.
    """

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

    total_neto: float = total_ingresos - total_deducciones

    print(f"""
🧾 LIQUIDACIÓN DETALLADA
-------------------------------
💰 Salario base:         ${salario_base:,.2f}
🕐 Horas extra diurnas:  ${pago_extra_diurna:,.2f}
🌙 Horas extra nocturnas:${pago_extra_nocturna:,.2f}
☀️  Horas dominicales:   ${pago_extra_dominical:,.2f}
🚍 Auxilio transporte:   ${auxilio_transporte:,.2f}
-------------------------------
💸 Ingresos totales:     ${total_ingresos:,.2f}
🏥 Salud (4%):           -${descuento_salud:,.2f}
👴 Pensión (4%):         -${descuento_pension:,.2f}
-------------------------------
✅ Neto a pagar:         ${total_neto:,.2f}
""")

    return total_neto


def calcular_provisiones(salario_mensual: float, dias_trabajados: int) -> float:
    """Calcula provisiones de prestaciones sociales (cesantías, intereses, prima, vacaciones)."""
    cesantias: float = salario_mensual * dias_trabajados / DIVISOR_CESANTIAS
    intereses_cesantias: float = cesantias * PORC_INTERESES_CESANTIAS
    prima: float = salario_mensual * dias_trabajados / DIVISOR_PRIMA
    vacaciones: float = salario_mensual * dias_trabajados / DIVISOR_VACACIONES

    total_provisiones = cesantias + intereses_cesantias + prima + vacaciones

    print(f"""
📦 PROVISIONES
-------------------------------
Cesantías:              ${cesantias:,.2f}
Intereses cesantías:    ${intereses_cesantias:,.2f}
Prima:                  ${prima:,.2f}
Vacaciones:             ${vacaciones:,.2f}
-------------------------------
Total provisiones:      ${total_provisiones:,.2f}
""")

    return total_provisiones


def calcular_aportes_empleador(salario_mensual: float) -> float:
    """Calcula el total de aportes a seguridad social y parafiscales a cargo del empleador."""
    aporte_salud: float = salario_mensual * PORC_SALUD_EMP
    aporte_pension: float = salario_mensual * PORC_PENSION_EMP
    aporte_arl: float = salario_mensual * PORC_ARL
    aporte_caja_compensacion: float = salario_mensual * PORC_CAJA_COMPENSACION
    aporte_icbf: float = salario_mensual * PORC_ICBF
    aporte_sena: float = salario_mensual * PORC_SENA

    total_aportes = (
        aporte_salud
        + aporte_pension
        + aporte_arl
        + aporte_caja_compensacion
        + aporte_icbf
        + aporte_sena
    )

    print(f"""
🏢 APORTES EMPLEADOR
-------------------------------
Salud:                  ${aporte_salud:,.2f}
Pensión:                ${aporte_pension:,.2f}
ARL:                    ${aporte_arl:,.2f}
Caja de Compensación:   ${aporte_caja_compensacion:,.2f}
ICBF:                   ${aporte_icbf:,.2f}
SENA:                   ${aporte_sena:,.2f}
-------------------------------
Total aportes:          ${total_aportes:,.2f}
""")

    return total_aportes


# --------------------------------------------
# 🔹 FUNCIÓN PRINCIPAL PARA GUARDAR EN BD
# --------------------------------------------

def registrar_liquidacion(
    empleado_id: int,
    salario_mensual: float,
    dias_trabajados: int,
    horas_extra_diurnas: int = 0,
    horas_extra_nocturnas: int = 0,
    horas_extra_dominicales: int = 0,
    aplica_auxilio_transporte: bool = True
):
    """Registra la liquidación completa de un empleado en la base de datos."""
    conn = get_connection()
    if conn:
        try:
            total_neto = calcular_neto_a_pagar(
                salario_mensual,
                dias_trabajados,
                horas_extra_diurnas,
                horas_extra_nocturnas,
                horas_extra_dominicales,
                aplica_auxilio_transporte
            )

            provisiones = calcular_provisiones(salario_mensual, dias_trabajados)
            aportes_empleador = calcular_aportes_empleador(salario_mensual)

            total_final = total_neto + provisiones + aportes_empleador

            cur = conn.cursor()
            cur.execute("""
                INSERT INTO liquidaciones (empleado_id, total)
                VALUES (%s, %s)
                RETURNING id;
            """, (empleado_id, total_final))
            conn.commit()
            liquidacion_id = cur.fetchone()[0]
            cur.close()

            print(f"💾 Liquidación registrada con ID {liquidacion_id} y total de ${total_final:,.2f}")

            return liquidacion_id

        except Exception as e:
            print("❌ Error al registrar liquidación:", e)
        finally:
            conn.close()