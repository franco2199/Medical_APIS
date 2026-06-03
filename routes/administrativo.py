from flask import Blueprint, request, jsonify
from models.administrativo import Administrativo


ws_administrativo = Blueprint('ws_administrativo',__name__)

administrativo = Administrativo()

@ws_administrativo.route('/administrativo/registrar', methods=['POST'])
def registrar_administrativo():

    try:

        data = request.get_json()

        campos = [
            'email',
            'password',
            'nombres',
            'apellidos',
            'dni',
            'telefono',
            'cargo'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':
                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = administrativo.registrar_administrativo(data)

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 400

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Administrativo registrado correctamente'
        }), 201

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_administrativo.route('/administrativo/listar', methods=['GET'])
def listar_administrativos():

    try:

        resultados = administrativo.listar_administrativos()

        return jsonify({
            'status': True,
            'data': resultados,
            'message': 'Lista de administrativos obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_administrativo.route('/administrativo/obtener/<id_administrativo>', methods=['GET'])
def obtener_administrativo(id_administrativo):

    try:

        resultado = administrativo.obtener_administrativo(
            id_administrativo
        )

        if not resultado:

            return jsonify({
                'status': False,
                'data': None,
                'message': 'Administrativo no encontrado'
            }), 404

        return jsonify({
            'status': True,
            'data': resultado,
            'message': 'Administrativo obtenido correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        

@ws_administrativo.route('/administrativo/actualizar/<id_administrativo>', methods=['PUT'])
def actualizar_administrativo(id_administrativo):

    try:

        data = request.get_json()

        campos = [
            'telefono',
            'cargo',
            'area'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':

                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = administrativo.actualizar_administrativo(
            id_administrativo,
            data
        )

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 404

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Administrativo actualizado correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_administrativo.route('/administrativo/eliminar/<id_administrativo>', methods=['DELETE'])
def eliminar_administrativo(id_administrativo):

    try:

        resultado = administrativo.eliminar_administrativo(
            id_administrativo
        )

        if resultado['error']:

            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 404

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Administrativo eliminado correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500