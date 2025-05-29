import psycopg2
import psycopg2.extras
from ..config import Config

def get_db_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASS
    )

def get_user_role(username):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT rol FROM usuario WHERE usuario=%s', [username])
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado['rol'] if resultado else None

def get_funcionario_cargo(nombre):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT nombre, cargo FROM funcionario WHERE nombre = %s', [nombre])
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado if resultado else {'nombre': nombre, 'cargo': '[Ingrese Cargo]'}

def get_sugerencias_cargos(nombre):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT nombre FROM funcionario WHERE LOWER(nombre) LIKE %s', ['%' + nombre.lower() + '%'])
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return [fila['nombre'] for fila in resultados]