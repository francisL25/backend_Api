from flask import Blueprint, request, jsonify, session
from ..services.document_service import crear_nota_interna, crear_nota_externa
from ..services.neural_model import model_response

document_bp = Blueprint('document', __name__)

@document_bp.route('/generar', methods=['POST'])
def generar():
    if 'username' not in session:
        return jsonify({'error': 'No autorizado'}), 401

    data = request.get_json()
    tipoDoc = data.get('tipoDoc')
    referencia = data.get('referencia')
    destino = data.get('destino')
    via = data.get('via', '')
    emisor = data.get('emisor', '')
    selected_suggestions = data.get('selectedSuggestions', [])

    if not tipoDoc or not referencia or not destino:
        return jsonify({'error': 'tipoDoc, referencia y destino son requeridos'}), 400

    cleaned_suggestions = [suggestion.split('   ')[0] for suggestion in selected_suggestions]
    prompt = model_response(referencia)
    if prompt != "Introduzca su texto":
        prompt = f"puedes escribir esto corregir ortografia y darle formato: {prompt}"

    try:
        if tipoDoc in ["notaInterna", "informe"]:
            ruta = crear_nota_interna(tipoDoc, destino, cleaned_suggestions, emisor, referencia, prompt)
            return jsonify({'message': 'Documento generado', 'file_path': ruta})
        elif tipoDoc == "notaExterna":
            ruta = crear_nota_externa(tipoDoc, destino, referencia, prompt)
            return jsonify({'message': 'Documento generado', 'file_path': ruta})
        else:
            return jsonify({'error': 'Tipo de documento inválido'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500