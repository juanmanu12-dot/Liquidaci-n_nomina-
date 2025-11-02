# --------------------------------------------
# test/test_empleado.py — Pruebas CRUD de empleados
# --------------------------------------------
import unittest
import sys, os

# Agregar la ruta de src al path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'src')
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from src.model.empleado import Empleado


class TestEmpleado(unittest.TestCase):
    """Pruebas unitarias del módulo Empleado."""

    def test_insertar(self):
        print("\n🧩 Probando inserción de empleado...")
        nuevo_id = Empleado.insertar("Juan Pérez", "Analista", 2500000)
        self.assertIsNotNone(nuevo_id, "❌ No se insertó el empleado correctamente.")

    def test_listar(self):
        print("\n📋 Probando listado de empleados...")
        empleados = Empleado.listar()
        self.assertIsInstance(empleados, list, "❌ No devolvió una lista de empleados.")

    def test_buscar(self):
        print("\n🔍 Probando búsqueda de empleado...")
        empleados = Empleado.listar()
        if empleados:
            encontrado = Empleado.buscar_por_id(empleados[-1][0])
            self.assertIsNotNone(encontrado, "❌ No se encontró el empleado recién insertado.")
        else:
            self.skipTest("⚠️ No hay empleados para buscar.")

    def test_eliminar(self):
        print("\n🗑️ Probando eliminación de empleado...")
        empleados = Empleado.listar()
        if empleados:
            ultimo_id = empleados[-1][0]
            eliminado = Empleado.eliminar(ultimo_id)
            self.assertTrue(eliminado, "❌ No se eliminó el empleado correctamente.")
        else:
            self.skipTest("⚠️ No hay empleados para eliminar.")


if __name__ == "__main__":
    unittest.main()
