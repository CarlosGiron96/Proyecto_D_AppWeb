from flask_login import UserMixin
from psycopg2.extras import RealDictCursor

class Usuario(UserMixin):
    def __init__(self, id_usuario, username, password_hash, nombre):
        self.id = id_usuario
        self.username = username
        self.password_hash = password_hash
        self.nombre = nombre

    @staticmethod
    def get_by_id(id_usuario, get_db_connection):
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            return Usuario(
                id_usuario=user_data['id_usuario'],
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                nombre=user_data['nombre']
            )
        return None

    @staticmethod
    def get_by_username(username, get_db_connection):
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            return Usuario(
                id_usuario=user_data['id_usuario'],
                username=user_data['username'],
                password_hash=user_data['password_hash'],
                nombre=user_data['nombre']
            )
        return None