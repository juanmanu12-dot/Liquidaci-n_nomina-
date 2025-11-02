# --------------------------------------------
# src/model/empleado.py — Clase Empleado (CRUD completo y compatible con BD)
# --------------------------------------------
from src.database import get_connection


class Empleado:
    """Clase para manejar operaciones CRUD de la tabla empleados en PostgreSQL."""

    # ------------------------------------------------------------
    # CREAR EMPLEADO
    # ------------------------------------------------------------
    @staticmethod
    def insertar(nombre: str, cargo: str, salario: float):
        """
        Inserta un nuevo empleado en la tabla 'empleados'.
        Retorna el ID del empleado insertado.
        """
        conn = get_connection()
        if not conn:
            print("❌ No se pudo establecer conexión con la base de datos.")
            return None

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO empleados (nombre, cargo, salario)
                VALUES (%s, %s, %s)
                RETURNING id;
            """, (nombre, cargo, salario))
            empleado_id = cur.fetchone()[0]
            conn.commit()
            cur.close()

            print(f"✅ Empleado '{nombre}' insertado con ID {empleado_id}")
            return empleado_id

        except Exception as e:
            print("❌ Error al insertar empleado:", e)
            conn.rollback()
            return None
        finally:
            conn.close()

    # ------------------------------------------------------------
    # LISTAR EMPLEADOS
    # ------------------------------------------------------------
    @staticmethod
    def listar():
        """
        Retorna una lista con todos los empleados registrados.
        """
        conn = get_connection()
        if not conn:
            print("❌ No se pudo establecer conexión con la base de datos.")
            return []

        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, cargo, salario FROM empleados ORDER BY id;")
            empleados = cur.fetchall()
            cur.close()

            if empleados:
                print("📋 Empleados registrados:")
                for emp in empleados:
                    print(f"   → ID:{emp[0]} | Nombre:{emp[1]} | Cargo:{emp[2]} | Salario:${emp[3]:,.2f}")
            else:
                print("⚠️ No hay empleados registrados en la base de datos.")

            return empleados

        except Exception as e:
            print("❌ Error al listar empleados:", e)
            return []
        finally:
            conn.close()

    # ------------------------------------------------------------
    # BUSCAR EMPLEADO POR ID
    # ------------------------------------------------------------
    @staticmethod
    def buscar_por_id(empleado_id: int):
        """
        Busca un empleado por su ID.
        Retorna una tupla con los datos del empleado o None si no existe.
        """
        conn = get_connection()
        if not conn:
            print("❌ No se pudo establecer conexión con la base de datos.")
            return None

        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, cargo, salario FROM empleados WHERE id = %s;", (empleado_id,))
            empleado = cur.fetchone()
            cur.close()

            if empleado:
                print(f"🔍 Empleado encontrado: ID={empleado[0]}, Nombre={empleado[1]}, Cargo={empleado[2]}, Salario=${empleado[3]:,.2f}")
            else:
                print("⚠️ No se encontró ningún empleado con ese ID.")

            return empleado

        except Exception as e:
            print("❌ Error al buscar empleado:", e)
            return None
        finally:
            conn.close()

    # ------------------------------------------------------------
    # ACTUALIZAR EMPLEADO
    # ------------------------------------------------------------
    @staticmethod
    def actualizar(empleado_id: int, nombre: str, cargo: str, salario: float):
        """
        Actualiza los datos de un empleado por su ID.
        """
        conn = get_connection()
        if not conn:
            print("❌ No se pudo establecer conexión con la base de datos.")
            return False

        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE empleados
                SET nombre = %s, cargo = %s, salario = %s
                WHERE id = %s;
            """, (nombre, cargo, salario, empleado_id))
            conn.commit()
            actualizado = cur.rowcount > 0
            cur.close()

            if actualizado:
                print(f"✏️ Empleado con ID {empleado_id} actualizado correctamente.")
            else:
                print("⚠️ No se encontró un empleado con ese ID.")

            return actualizado

        except Exception as e:
            print("❌ Error al actualizar empleado:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

    # ------------------------------------------------------------
    # ELIMINAR EMPLEADO
    # ------------------------------------------------------------
    @staticmethod
    def eliminar(empleado_id: int):
        """
        Elimina un empleado por su ID.
        Retorna True si se eliminó, False si no se encontró o hubo error.
        """
        conn = get_connection()
        if not conn:
            print("❌ No se pudo establecer conexión con la base de datos.")
            return False

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM empleados WHERE id = %s;", (empleado_id,))
            conn.commit()
            eliminado = cur.rowcount > 0
            cur.close()

            if eliminado:
                print(f"🗑️ Empleado con ID {empleado_id} eliminado correctamente.")
            else:
                print("⚠️ No se encontró un empleado con ese ID.")

            return eliminado

        except Exception as e:
            print("❌ Error al eliminar empleado:", e)
            conn.rollback()
            return False
        finally:
            conn.close()
