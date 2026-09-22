import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Establece conexión a PostgreSQL (Soporta entorno local y producción en Render)."""
    # Render proporciona DATABASE_URL en sus variables de entorno
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # En Render la URL suele iniciar con postgres://, pero psycopg2 requiere postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        conn = psycopg2.connect(database_url)
    else:
        # Configuración local de PostgreSQL
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            user='postgres',        # Tu usuario local de PostgreSQL
            password='tu_password', # Tu contraseña local de PostgreSQL
            dbname='cocoffe_db'
        )
    return conn