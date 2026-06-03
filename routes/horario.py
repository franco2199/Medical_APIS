from flask import Blueprint, request, jsonify
from models.horario import Horario

ws_horario = Blueprint('ws_horario', __name__)

horario = Horario()

@ws_horario.route('/horarios/disponibles', methods=['POST'])
def horario_disponibles():

    try:

        data = request.get_json()

        campos = [
            'especialidad_id',
            'fecha'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':

                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = horario.horario_disponibles(
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
            'message': 'Horarios disponibles obtenidos correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500