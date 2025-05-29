from flask import Blueprint, request, jsonify, session
from ..services.database import get_db_connection
import psycopg2.extras
import hashlib


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    if 'username' in session:
        return jsonify({'message': 'Ya estás autenticado'}), 200

    data = request.get_json()
    usuario = data.get('usuario')
    codigo = data.get('password')
    contraseña = hashlib.sha256(codigo.encode()).hexdigest() if codigo else None
    
    if not usuario or not contraseña:
        return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT password, rol FROM usuario WHERE usuario=%s', [usuario])
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado and contraseña == resultado['password']:
        session['username'] = usuario
        session['rol'] = resultado['rol']
        return jsonify({'message': 'Inicio de sesión exitoso', 'rol': resultado['rol']})
    else:
        return jsonify({'error': 'Credenciales incorrectas' if resultado else 'Usuario no encontrado'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    if 'username' in session:
        session.pop('username', None)
        session.pop('rol', None)
        return jsonify({'message': 'Sesión cerrada exitosamente'})
    return jsonify({'error': 'No hay sesión activa'}), 400