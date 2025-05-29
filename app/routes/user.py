from flask import Blueprint, request, jsonify, session
from ..services.database import get_db_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/guardar_usuario', methods=['POST'])
def guardar_usuario():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.get_json()
    rol = 1 if data.get('rol') == 'administrador' else 2
    nombre = data.get('nombre')
    correo = data.get('correo')
    contrasena = data.get('contrasena')

    if not all([nombre, correo, contrasena]):
        return jsonify({'error': 'Nombre, correo y contraseña son requeridos'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuario (usuario, correo, password, rol) VALUES (%s,%s,%s,%s)',
                   [nombre, correo, contrasena, rol])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Usuario guardado exitosamente'})

@user_bp.route('/eliminar_usuario/<int:user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuario WHERE id = %s', [user_id])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Usuario eliminado correctamente'})