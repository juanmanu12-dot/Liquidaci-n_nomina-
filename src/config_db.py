import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def get_connection():
    try:
        print("🚀 Ejecutando prueba de conexión segura a Render...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            sslmode="require"
        )
        print("✅ Conexión establecida correctamente con Render.")
        return conn
    except psycopg2.OperationalError as e:
        print("❌ Error operacional al conectar a la base de datos:\n", e)
        return None
    except Exception as e:
        print("❌ Error general en la conexión:\n", e)
        return None
