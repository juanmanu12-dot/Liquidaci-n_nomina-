# --------------------------------------------
# test/test_database.py — Prueba conexión y tablas en Render
# --------------------------------------------
import unittest
from src.database import get_connection, crear_tablas_desde_sql


class TestDatabase(unittest.TestCase):
    """Pruebas unitarias para la base de datos en Render."""

    def test_conexion_exitosa(self):
        print("\n🔌 Probando conexión a la base de datos Render...")
        conn = get_connection()
        self.assertIsNotNone(conn, "❌ No se pudo conectar a la base de datos Render.")
        if conn:
            conn.close()

    def test_creacion_tablas(self):
        print("\n🧱 Probando creación de tablas...")
        crear_tablas_desde_sql()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tablas = [t[0] for t in cur.fetchall()]
        cur.close()
        conn.close()

        self.assertIn("empleados", tablas, "❌ Falta la tabla 'empleados'.")
        self.assertIn("liquidaciones", tablas, "❌ Falta la tabla 'liquidaciones'.")


if __name__ == "__main__":
    unittest.main()
