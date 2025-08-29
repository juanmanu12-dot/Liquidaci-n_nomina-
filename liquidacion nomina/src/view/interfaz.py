import sys
sys.path.append("src")

from model import test


try:
    
    
    
    nombre = input("Ingrese el nombre del empleado: ")
    salario = float(input("Ingrese el salario mensual: "))
    dias_trabajados = int(input("Ingrese los días trabajados: "))
    horas_extra_diurnas = int(input("Ingrese las horas extra diurnas: "))
    horas_extra_nocturnas = int(input("Ingrese las horas extra nocturnas: "))
    horas_extra_dominicales = int(input("Ingrese las horas extra dominicales: "))
    aplica_aux = input("¿Aplica auxilio de transporte? (s/n): ").strip().lower()

 
    
  
    neto = test.calcular_neto_a_pagar(
        salario,
        dias_trabajados,
        horas_extra_diurnas,
        horas_extra_nocturnas,
        horas_extra_dominicales,
        aplica_aux == "s"
    )

    provisiones = test.calcular_provisiones(salario, dias_trabajados)
    aportes = test.calcular_aportes_empleador(salario)

    
    
    print("\n--- LIQUIDACIÓN DE NÓMINA ---")
    print(f"Empleado                  : {nombre}")
    print(f"Neto a pagar              : {neto}")
    print(f"Total provisiones         : {provisiones}")
    print(f"Aportes del empleador     : {aportes}")

except ValueError:
    print("Por favor verifique los datos ingresados (se esperaba un número).")

except Exception as e:

    print("No se puede calcular la nómina: " + str(e))
