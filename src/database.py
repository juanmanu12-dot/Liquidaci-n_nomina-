# --------------------------------------------
# database.py — Conexión segura a PostgreSQL Render (SSL + .env)
# --------------------------------------------
import psycopg2
from src.config_db import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT


# --------------------------------------------
# Establecer conexión segura
# --------------------------------------------
def get_connection():
    """
    Establece y retorna una conexión segura a la base de datos PostgreSQL en Render.
    Usa SSL obligatorio (sslmode='require') y variables del archivo .env.
    Si la conexión falla, retorna None.
    """
    print("🚀 Ejecutando prueba de conexión segura a Render...")

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            sslmode="require"  # Render exige conexión SSL/TLS
        )
        print("✅ Conexión exitosa a la base de datos Render (SSL activado).")
        return conn

    except psycopg2.OperationalError as e:
        print("❌ Error operacional al conectar a la base de datos:")
        print(e)
        return None

    except Exception as e:
        print("❌ Error general al conectar:")
        print(e)
        return None


# --------------------------------------------
# Crear tablas si no existen
# --------------------------------------------
def crear_tablas_desde_sql():
    """
    Crea las tablas principales del sistema si aún no existen.
    Incluye 'empleados' y 'liquidaciones'.
    """
    sql_script = """
    CREATE TABLE IF NOT EXISTS empleados (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        cargo VARCHAR(100),
        salario NUMERIC(12, 2)
    );

    CREATE TABLE IF NOT EXISTS liquidaciones (
        id SERIAL PRIMARY KEY,
        empleado_id INT REFERENCES empleados(id),
        fecha DATE DEFAULT CURRENT_DATE,
        total NUMERIC(12, 2)
    );
    """

    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(sql_script)
            conn.commit()
            cur.close()
            print("✅ Tablas creadas o verificadas correctamente.")
        except Exception as e:
            print("❌ Error al crear/verificar las tablas:", e)
        finally:
            conn.close()
    else:
        print("⚠️ No se pudo establecer conexión para crear las tablas.")


# --------------------------------------------
# Mostrar todas las tablas existentes
# --------------------------------------------
def mostrar_tablas():
    """
    Consulta y muestra las tablas existentes en el esquema 'public'.
    """
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            print("🔍 Consultando las tablas existentes en la base de datos...")

            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
            """)

            tablas = cur.fetchall()

            if tablas:
                print("📋 Tablas encontradas:")
                for t in tablas:
                    print(f"   - {t[0]}")
            else:
                print("⚠️ No se encontraron tablas en el esquema 'public'.")

            cur.close()

        except Exception as e:
            print("❌ Error al consultar las tablas:", e)

        finally:
            conn.close()
            print("🔒 Conexión cerrada correctamente.")
    else:
        print("❌ No se pudo establecer conexión con la base de datos.")


# --------------------------------------------
# Ejecutar consultas personalizadas
# --------------------------------------------
def ejecutar_consulta(query, params=None, fetch=False):
    """
    Ejecuta una consulta SQL de manera segura.
    Parámetros:
      - query: la sentencia SQL
      - params: tupla con los valores (%s, ...)
      - fetch: si True, devuelve resultados (para SELECT)
    """
    conn = get_connection()
    if not conn:
        print("⚠️ No se pudo establecer conexión para ejecutar la consulta.")
        return None

    try:
        cur = conn.cursor()
        cur.execute(query, params)

        resultados = cur.fetchall() if fetch else None
        conn.commit()
        cur.close()
        conn.close()

        if fetch:
            return resultados
        else:
            print("✅ Consulta ejecutada correctamente.")

    except Exception as e:
        print("❌ Error al ejecutar la consulta:", e)
        if conn:
            conn.rollback()
        return None


# --------------------------------------------
# Punto de entrada principal (prueba)
# --------------------------------------------
if __name__ == "__main__":
    print("🚀 Iniciando script desde __main__ ...")
    crear_tablas_desde_sql()
    mostrar_tablas()

    # Ejemplo: Insertar un empleado de prueba
    insertar_empleado = """
    INSERT INTO empleados (nombre, cargo, salario)
    VALUES (%s, %s, %s);
    """
    ejecutar_consulta(insertar_empleado, ("Ana Torres", "Analista", 2900000))

    # Ejemplo: Consultar empleados
    consulta = "SELECT id, nombre, cargo, salario FROM empleados;"
    resultados = ejecutar_consulta(consulta, fetch=True)
    if resultados:
        print("📊 Empleados registrados:")
        for fila in resultados:
            print(fila)
