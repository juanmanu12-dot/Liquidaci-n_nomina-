import sys
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(BASE_DIR)

from src.model import liquidacion


def ejecutar_liquidacion():


    try:
        # ENTRADAS DEL USUARIO
        nombre_empleado = input("Ingrese el nombre del empleado: ").strip()
        salario_mensual = float(input("Ingrese el salario mensual: "))
        dias_trabajados = int(input("Ingrese los días trabajados: "))
        horas_extra_diurnas = int(input("Ingrese las horas extra diurnas: "))
        horas_extra_nocturnas = int(input("Ingrese las horas extra nocturnas: "))
        horas_extra_dominicales = int(input("Ingrese las horas extra dominicales: "))
        aplica_auxilio = input("¿Aplica auxilio de transporte? (s/n): ").strip().lower() == "s"

        # PROCESOS
        neto_a_pagar = liquidacion.calcular_neto_a_pagar(
            salario_mensual,
            dias_trabajados,
            horas_extra_diurnas,
            horas_extra_nocturnas,
            horas_extra_dominicales,
            aplica_auxilio
        )

        total_provisiones = liquidacion.calcular_provisiones(salario_mensual, dias_trabajados)
        aportes_empleador = liquidacion.calcular_aportes_empleador(salario_mensual)

        # SALIDAS
        print("\n======= LIQUIDACIÓN DE NÓMINA =======")
        print(f"Empleado              : {nombre_empleado}")
        print(f"Neto a pagar          : ${neto_a_pagar:,.2f}")
        print(f"Total provisiones     : ${total_provisiones:,.2f}")
        print(f"Aportes del empleador : ${aportes_empleador:,.2f}")

    except ValueError:
        print("\n⚠️ Error: Se esperaba un número en uno de los campos ingresados.")
    except Exception as error:
        print(f"\n⚠️ No se pudo calcular la nómina. Detalle: {error}")


if __name__ == "__main__":
    ejecutar_liquidacion()
