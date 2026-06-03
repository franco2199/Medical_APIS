from flask import Blueprint, request, jsonify
from models.cita import Cita

ws_cita = Blueprint('ws_cita', __name__)

cita = Cita()

@ws_cita.route('/cita/registrar', methods=['POST'])
def registrar_cita():

    try:

        data = request.get_json()

        campos = [
            'paciente_id',
            'horario_disponible_id',
            'motivo',
            'paciente_oncologico',
            'creado_por_usuario_id'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data:

                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = cita.registrar_cita(data)

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 400

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Cita registrada correctamente'
        }), 201

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_cita.route('/paciente/<id_paciente>/cita', methods=['GET'])
def listar_citas_paciente(id_paciente):

    try:

        resultado = cita.listar_citas_paciente(
            id_paciente
        )

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 400

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Lista de citas obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_cita.route('/cita/<id_cita>/cancelar', methods=['PUT'])
def cancelar_cita(id_cita):

    try:

        resultado = cita.cancelar_cita(
            id_cita
        )

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 400

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Cita cancelada correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_cita.route('/medico/<id_medico>/cita', methods=['GET'])
def listar_citas_medico(id_medico):

    try:

        resultado = cita.listar_citas_medico(
            id_medico
        )

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 400

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Lista de citas del médico obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500