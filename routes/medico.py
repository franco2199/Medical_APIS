from flask import Blueprint, request, jsonify, send_from_directory
from models.medico import Medico
from tools.jwt_utils import generar_token
from tools.jwt_required import jwt_token_requerido


ws_medico = Blueprint('ws_medico', __name__)

medico = Medico()

@ws_medico.route('/medico/registrar', methods=['POST'])
def registrar_medico():

    try:

        data = request.get_json()

        campos = [
            'email',
            'password',
            'nombres',
            'apellidos',
            'dni',
            'cmp',
            'telefono',
            'consultorio',
            'estado_medico_id'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':
                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = medico.registrar_medico(data)

        if resultado['error']:
            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 400

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Médico registrado correctamente'
        }), 201

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        

@ws_medico.route('/medico/listar', methods=['GET'])
def listar_medicos():

    try:

        resultados = medico.listar_medicos()

        return jsonify({
            'status': True,
            'data': resultados,
            'message': 'Lista de médicos obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        

@ws_medico.route('/medico/obtener/<id_medico>', methods=['GET'])
def obtener_medico(id_medico):

    try:

        resultado = medico.obtener_medico(id_medico)

        if not resultado:
            return jsonify({
                'status': False,
                'data': None,
                'message': 'Médico no encontrado'
            }), 404

        return jsonify({
            'status': True,
            'data': resultado,
            'message': 'Médico obtenido correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_medico.route('/medicos/actualizar/<id_medico>', methods=['PUT'])
def actualizar_medico(id_medico):

    try:

        data = request.get_json()

        campos = [
            'telefono',
            'consultorio',
            'estado_medico_id'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':
                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = medico.actualizar_medico(
            id_medico,
            data
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
            'message': 'Médico actualizado correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_medico.route('/medico/eliminar/<id_medico>', methods=['DELETE'])
def eliminar_medico(id_medico):

    try:

        resultado = medico.eliminar_medico(id_medico)

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 404

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Médico eliminado correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500