from flask import Blueprint, request, jsonify, send_from_directory
from models.paciente import Paciente
from tools.jwt_utils import generar_token
from tools.jwt_required import jwt_token_requerido
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from tools.security import password_validate

ws_paciente = Blueprint('ws_paciente', __name__)

paciente = Paciente()

#Crear un endpoint para registrar nuevo paciente
@ws_paciente.route('/paciente/registrar', methods=['POST'])
def registrar_paciente():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.get_json()
    
    #pasar los datos a variables
    #usuario_id, nombres, apellidos, dni, celular, genero
    usuario_id = data.get('usuario_id')
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    dni = data.get('dni')
    celular = data.get('celular')
    genero = data.get('genero')
    
    
    #Validar si contamos con los parámetros de email y clave
    if not all([usuario_id, nombres, apellidos, dni, celular, genero]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Registrar al usuario
    try:
        resultado, mensaje = paciente.registrar_paciente(usuario_id, nombres, apellidos, dni, celular, genero)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Paciente registrado'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
    

@ws_paciente.route('/paciente/listar', methods=['GET'])
def listar_pacientes():

    try:

        resultados = paciente.listar_pacientes()

        return jsonify({
            'status': True,
            'data': resultados,
            'message': 'Lista de pacientes obtenida correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
        

@ws_paciente.route('/paciente/obtener/<id_paciente>', methods=['GET'])
def obtener_paciente(id_paciente):

    try:

        resultado = paciente.obtener_paciente(id_paciente)

        if not resultado:
            return jsonify({
                'status': False,
                'data': None,
                'message': 'Paciente no encontrado'
            }), 404

        return jsonify({
            'status': True,
            'data': resultado,
            'message': 'Paciente obtenido correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        

@ws_paciente.route('/paciente/actualizar/<id_paciente>', methods=['PUT'])
def actualizar_paciente(id_paciente):

    try:

        data = request.get_json()

        campos = [
            'nombres',
            'apellidos',
            'celular',
            'fecha_nacimiento',
            'genero'
        ]

        # VALIDAR CAMPOS
        for campo in campos:

            if campo not in data or data[campo] == '':
                return jsonify({
                    'status': False,
                    'data': None,
                    'message': f'El campo {campo} es obligatorio'
                }), 400

        resultado = paciente.actualizar_paciente(
            id_paciente,
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
            'message': 'Paciente actualizado correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500
        
@ws_paciente.route('/paciente/eliminar/<id_paciente>', methods=['DELETE'])
def eliminar_paciente(id_paciente):

    try:

        resultado = paciente.eliminar_paciente(id_paciente)

        if resultado['error']:
            return jsonify({
                'status': False,
                'data': None,
                'message': resultado['message']
            }), 404

        return jsonify({
            'status': True,
            'data': resultado['data'],
            'message': 'Paciente eliminado correctamente'
        }), 200

    except Exception as e:

        return jsonify({
            'status': False,
            'data': None,
            'message': str(e)
        }), 500