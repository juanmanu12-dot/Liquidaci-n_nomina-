# test/test_empleado.py

from src.model.empleado import Empleado


def probar_insertar():
    print("\n🧩 Probando inserción de empleados...")
    Empleado.insertar("Laura Gómez", "Secretaria", 1800000)
    Empleado.insertar("Andrés Ruiz", "Ingeniero de Sistemas", 4200000)


def probar_listar():
    print("\n📋 Listando empleados registrados...")
    empleados = Empleado.listar()
    if empleados:
        for emp in empleados:
            print(emp)
    else:
        print("⚠️ No hay empleados registrados.")
    return empleados


def probar_buscar():
    print("\n🔍 Buscando empleado con ID 1...")
    Empleado.buscar_por_id(1)


def probar_eliminar():
    print("\n🗑️ Probando eliminación de empleado...")
    empleados = Empleado.listar()
    if empleados:
        ultimo_id = empleados[-1][0]
        Empleado.eliminar(ultimo_id)
    else:
        print("⚠️ No hay empleados para eliminar.")


if __name__ == "__main__":
    print("🚀 Iniciando pruebas del módulo Empleado...")

    probar_insertar()
    probar_listar()
    probar_buscar()
    probar_eliminar()

    print("\n✅ Pruebas finalizadas.")
