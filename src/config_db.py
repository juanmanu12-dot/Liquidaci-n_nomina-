# --------------------------------------------
# config_db.py — Configuración segura con dotenv
# --------------------------------------------
import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()

# Variables de conexión
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Construcción de la URL de conexión completa
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
