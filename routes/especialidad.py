from flask import Blueprint, request, jsonify
from models.especialidad import Especialidad


ws_especialidad = Blueprint('ws_especialidad', __name__)

especialidad = Especialidad()


@ws_especialidad.route('/especialidad/registrar', methods=['POST'])
def registrar_especialidad():

    try:

        data = request.get_json()

        campos = [
            'nombre',
            'descripcion'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':

                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = especialidad.registrar_especialidad(
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
            'message': 'Especialidad registrada correctamente'
        }), 201

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        

@ws_especialidad.route('/especialidad/listar', methods=['GET'])
def listar_especialidades():

    try:

        resultados = especialidad.listar_especialidades()

        return jsonify({
            'status': True,
            'data': resultados,
            'message': 'Lista de especialidades obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_especialidad.route('/especialidad/obtener/<id_especialidad>', methods=['GET'])
def obtener_especialidad(id_especialidad):

    try:

        resultado = especialidad.obtener_especialidad(
            id_especialidad
        )

        if not resultado:

            return jsonify({
                'status': False,
                'data': None,
                'message': 'Especialidad no encontrada'
            }), 404

        return jsonify({
            'status': True,
            'data': resultado,
            'message': 'Especialidad obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        

@ws_especialidad.route('/especialidad/actualizar/<id_especialidad>', methods=['PUT'])
def actualizar_especialidad(id_especialidad):

    try:

        data = request.get_json()

        campos = [
            'nombre',
            'descripcion'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':

                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = especialidad.actualizar_especialidad(
            id_especialidad,
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
            'message': 'Especialidad actualizada correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_especialidad.route('/especialidad/eliminar/<id_especialidad>', methods=['DELETE']
)
def eliminar_especialidad(id_especialidad):

    try:

        resultado = especialidad.eliminar_especialidad(
            id_especialidad
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
            'message': 'Especialidad eliminada correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500