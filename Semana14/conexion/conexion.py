import mysql.connector

def get_db_connection():
    """Establece y retorna la conexión activa con la base de datos MySQL de Cocoffe."""
    connection = mysql.connector.connect(
        host='localhost',
        user='root',          # Ajusta según las credenciales de tu servidor MySQL
        password='',          # Ingresa la contraseña de tu MySQL
        database='cocoffe_db' # Nombre de la base de datos
    )
    return connection