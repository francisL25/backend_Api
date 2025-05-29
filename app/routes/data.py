from flask import Blueprint, request, jsonify, session
from ..services.database import get_db_connection, get_sugerencias_cargos
import pandas as pd
import psycopg2

data_bp = Blueprint('data', __name__)
dataset = pd.read_csv('app/config/datosNormalizado3.csv')
columna_sugerencias = dataset['referencia'].unique()

@data_bp.route('/obtener_datos', methods=['GET'])
def obtener_datos():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT nombre, cargo, id FROM funcionario')
    nombres = cursor.fetchall()
    cursor.close()
    conn.close()
    data = [{'id': row['id'], 'nombre': row['nombre'], 'cargo': row['cargo']} for row in nombres]
    return jsonify(data)

@data_bp.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT id, usuario, correo FROM usuario')
    nombres = cursor.fetchall()
    cursor.close()
    conn.close()
    data = [{'id': row['id'], 'nombre': row['usuario'], 'correo': row['correo']} for row in nombres]
    return jsonify(data)

@data_bp.route('/sugerencias', methods=['GET'])
def obtener_sugerencias():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    referencia = request.args.get('referencia', '')
    if not referencia:
        return jsonify({'suggestions': []})
    sugerencias = [str(sug) for sug in columna_sugerencias if isinstance(sug, str) and referencia.lower() in sug.lower()]
    return jsonify({'suggestions': sugerencias})

@data_bp.route('/sugerenciaCargo', methods=['GET'])
def obtener_sugerencias_cargos():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    nombre = request.args.get('destino', '')
    if not nombre:
        return jsonify({'suggestions': []})
    sugerencias = get_sugerencias_cargos(nombre)
    return jsonify({'suggestions': sugerencias})

@data_bp.route('/agregarNombreCargo', methods=['POST'])
def agregar_nombre_cargo():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    nombre = data.get('nombre')
    cargo = data.get('cargo')
    if not nombre or not cargo:
        return jsonify({'error': 'Nombre y cargo son requeridos'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO funcionario (nombre, cargo) VALUES (%s,%s)', [nombre, cargo])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Datos agregados exitosamente'})

@data_bp.route('/editar/<int:id>', methods=['PUT'])
def editar(id):
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    data = request.get_json()
    nuevo_nombre = data.get('nombre')
    nuevo_cargo = data.get('cargo')
    if not nuevo_nombre or not nuevo_cargo:
        return jsonify({'error': 'Nombre y cargo son requeridos'}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE funcionario SET nombre = %s, cargo = %s WHERE id = %s',
                   [nuevo_nombre, nuevo_cargo, id])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Datos actualizados exitosamente'})

@data_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar(id):
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM funcionario WHERE id = %s', [id])
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Elemento eliminado exitosamente'})