import sys
sys.path.append("src")

from model import liquidacion

try:
    print("=== 💼 Sistema de Liquidación de Nómina ===\n")


    nombre     = input("Ingrese el nombre del empleado: ")
    horas      = float(input("Ingrese el número de horas trabajadas: "))
    valor_hora = float(input("Ingrese el valor de la hora ($): "))
    dias       = int(input("Ingrese el número de días trabajados en el mes: "))

    if horas <= 0:
        raise ValueError("❌ Las horas trabajadas deben ser mayores a cero.")
    if valor_hora <= 0:
        raise ValueError("❌ El valor de la hora debe ser mayor a cero.")
    if dias <= 0 or dias > 30:
        raise ValueError("❌ Los días trabajados deben estar entre 1 y 30.")

    salario_basico       = liquidacion.salario_basico(horas, valor_hora)
    auxilio_transporte   = liquidacion.auxilio_transporte(dias)
    deducciones          = liquidacion.deducciones(salario_basico)
    total_pagar          = liquidacion.total_pagar(salario_basico, auxilio_transporte, deducciones)

    print("\n✅ Resultados de la liquidación:")
    print(f"- Empleado: {nombre}")
    print(f"- Salario básico: ${salario_basico:,.2f}")
    print(f"- Auxilio de transporte: ${auxilio_transporte:,.2f}")
    print(f"- Deducciones: ${deducciones:,.2f}")
    print(f"- Total a pagar: ${total_pagar:,.2f}")

except (ValueError, Exception) as e:
    print(e)
    print("⚠️ Por favor verifique los datos ingresados.")
