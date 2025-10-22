# --------------------------------------------
# database.py — Conexión segura a PostgreSQL Render (SSL activado)
# --------------------------------------------

import psycopg2
import ssl
from config_db import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT


def get_connection():
    """Establece y retorna una conexión a la base de datos PostgreSQL en Render con SSL."""
    print("🚀 Ejecutando prueba de conexión segura...")

    try:
        # 🔒 Conexión con SSL forzado
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            sslmode="require"  # Fuerza el uso de SSL/TLS
        )

        print("✅ Conexión exitosa a la base de datos Render (SSL activado).")
        return conn

    except psycopg2.OperationalError as e:
        print("❌ Error operacional al conectar a la base de datos:")
        print(e)
        return None
    except Exception as e:
        print("❌ Error general al conectar:", e)
        return None


def mostrar_tablas():
    """Consulta y muestra las tablas existentes en el esquema 'public'."""
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


# ----------------------------------------------------------
# Punto de entrada del script (solo se ejecuta directamente)
# ----------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Iniciando script desde __main__ ...")
    mostrar_tablas()
