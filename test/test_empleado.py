# --------------------------------------------
# test/test_empleado.py — Pruebas CRUD de empleados
# --------------------------------------------
import unittest
import sys, os
from src.database import get_connection

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
        
        if not empleados:
            self.skipTest("⚠️ No hay empleados para eliminar.")
            return

        # Asumimos que el último empleado es el que tiene la dependencia
        ultimo_id = empleados[-1][0] 
        conn = None

        try:
            # --- INICIO DE LA CORRECCIÓN ---
            # 1. Conectarse y limpiar las liquidaciones de ese empleado
            print(f"🧹 Limpiando dependencias (liquidaciones) para el empleado ID: {ultimo_id}...")
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM liquidaciones WHERE empleado_id = %s", (ultimo_id,))
            conn.commit()
            cur.close()
            # --- FIN DE LA CORRECCIÓN ---

            # 2. Ahora sí, intentar eliminar al empleado
            print(f"🗑️ Eliminando al empleado ID: {ultimo_id}...")
            eliminado = Empleado.eliminar(ultimo_id)
            self.assertTrue(eliminado, "❌ No se eliminó el empleado (incluso después de limpiar dependencias).")
            print("✅ Empleado eliminado correctamente.")

        except Exception as e:
            if conn:
                conn.rollback()
            # Falla la prueba si hay cualquier error
            self.fail(f"❌ Error durante la eliminación: {e}") 
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    unittest.main()
