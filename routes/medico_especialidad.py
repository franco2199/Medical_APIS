from flask import Blueprint, request, jsonify
from models.medico_especialidad import MedicoEspecialidad

ws_medico_especialidad = Blueprint('ws_medico_especialidad', __name__)

medico_especialidad = MedicoEspecialidad()


@ws_medico_especialidad.route('/medico-especialidad/registrar', methods=['POST'])
def registrar_relacion():

    try:

        data = request.get_json()

        campos = [
            'medico_id',
            'especialidad_id'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':

                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = medico_especialidad.registrar_relacion(
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
            'message': 'Relación médico-especialidad registrada correctamente'
        }), 201

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        


@ws_medico_especialidad.route('/medico-especialidad/listar', methods=['GET'])
def listar_relaciones():

    try:

        resultados = medico_especialidad.listar_relaciones()

        return jsonify({
            'status': True,
            'data': resultados,
            'message': 'Lista de relaciones obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_medico_especialidad.route('/medico-especialidad/obtener/<id_relacion>', methods=['GET'])
def obtener_relacion(id_relacion):

    try:

        resultado = medico_especialidad.obtener_relacion(
            id_relacion
        )

        if not resultado:

            return jsonify({
                'status': False,
                'data': None,
                'message': 'Relación no encontrada'
            }), 404

        return jsonify({
            'status': True,
            'data': resultado,
            'message': 'Relación obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_medico_especialidad.route('/medico-especialidad/actualizar/<id_relacion>', methods=['PUT'])
def actualizar_relacion(id_relacion):

    try:

        data = request.get_json()

        campos = [
            'medico_id',
            'especialidad_id'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':

                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = medico_especialidad.actualizar_relacion(
            id_relacion,
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
            'message': 'Relación actualizada correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        
@ws_medico_especialidad.route('/medico-especialidad/eliminar/<id_relacion>',methods=['DELETE'])
def eliminar_relacion(id_relacion):

    try:

        resultado = medico_especialidad.eliminar_relacion(
            id_relacion
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
            'message': 'Relación eliminada correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500