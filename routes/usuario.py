from flask import Blueprint, request, jsonify, send_from_directory
from models.usuario import Usuario
from tools.jwt_utils import generar_token
from tools.jwt_required import jwt_token_requerido
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from tools.security import password_validate


#Crear un módulo (servicio) para la gestión de usuarios: login, registro, cambiar contraseña
ws_usuario = Blueprint('ws_usuario', __name__)

#Instanciar al usuario
usuario = Usuario()

#Crear un end point para el inicio de sesión
@ws_usuario.route('/login', methods=['POST'])
def login():
    #obtener las credenciales que se recibe como dato de entrada
    data = request.get_json()
    
    #Almacenar las credenciales en variables locales
    email = data.get('email')
    clave = data.get('clave')
    
    #Validar si contamos con las credenciales 
    if not all([email, clave]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios' }), 400
    
    #Ejecutar el inicio de sesión
    try: 
        #Llamar al método login
        resultado = usuario.login(email, clave)
        
        if resultado: #Validar si hay resultado
            #Retirar la clave del resultado
            resultado.pop ('clave', None)
            
            #Generar el token jwt
            token = generar_token({'usuario_id': resultado['usuario_id']}, 60)
            
            #Incluir el token en el resultado del endpoint
            resultado['token'] = token
            
            #Imprimir el resultado
            return jsonify({'status': True, 'data': resultado, 'message': 'Inicio de sesión satisfactorio'}), 200
        
        else:  #credenciales incorrectas
            return jsonify({'status': False, 'data': None, 'message': 'Credenciales incorrectas'}), 401
            
        
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
    
    
#Crear un endpoint para obteber la foto del usuario
@ws_usuario.route('/usuario/foto/<id>', methods=['GET'])
@jwt_token_requerido
def obtener_foto(id):
    #validar si se cuenta con el id para obtener la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400

    try:
        resultado = usuario.obtener_foto(id)
        if resultado:
            return send_from_directory('uploads/fotos/usuarios', resultado['foto'])
        else:
            return send_from_directory('uploads/fotos/usuarios', 'default.png')
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
    

#Obtener datos del perfil por el id del usuario
@ws_usuario.route('/perfil/<id>', methods=['GET'])
@jwt_token_requerido
def obtener_perfil(id):
    #validar si se cuenta con el id para obtener la foto
    if not all([id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    try:
        resultado = usuario.obtener_perfil(id)
        if resultado:
            return jsonify({'status': True, 'data': resultado, 'message': 'Perfil obtenido correctamente'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': 'No se encontro perfil'}), 401
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    
    
@ws_usuario.route('/usuario/actualizar/foto', methods=['PUT'])
@jwt_token_requerido
def actualizar_foto():
    #pasar los datos a variables
    #id, foto
    id = request.form.get('id')
    foto = request.files.get('foto')
    
    #Validar si contamos con los parámetros de email y clave
    if not all([id, foto]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Actualizar la foto del usuario
    try:
        #Cargar la foto del usuario al servidor (storage)
        nombre_foto = None
        
        if foto:
            extension = os.path.splitext(foto.filename)[1] #obtiene: ".jpg", ".png", ".gif"
            nombre_foto = secure_filename(f"{id}{extension}") #obtiene: "3.jpg", "3.png"
            ruta_foto = os.path.join("uploads", "fotos", "usuarios", nombre_foto)
            foto.save(ruta_foto)
        
            resultado, mensaje = usuario.actualizar_foto(nombre_foto, id)
            if resultado:
                return jsonify({'status': True, 'data': None, 'message': 'Se ha actualizado la foto del usuario'}), 200
            else:
                return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
        else:
            return jsonify({'status': False, 'data': None, 'message': "La fotografía que intenta cargar no es válida"}), 500
        
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500
    


#Crear un endpoint para registrar nuevos usuarios
@ws_usuario.route('/usuario/actualizar/clave', methods=['PUT'])
@jwt_token_requerido
def actualizar_password():
    #Obtener los datos que se envian como parámetros de entrada
    data = request.get_json()
    
    #pasar los datos a variables
    #clave_actual, clave_nueva, clave_nueva_confirmada
    clave_actual = data.get('clave_actual')
    clave_nueva = data.get('clave_nueva')
    clave_nueva_confirmada = data.get('clave_nueva_confirmada')
    id = data.get('id')
    
    #Validar si contamos con los parámetros requeridos
    if not all([clave_actual, clave_nueva, clave_nueva_confirmada, id]):
        return jsonify({'status': False, 'data': None, 'message': 'Faltan datos obligatorios'}), 400
    
    #Validar que las nuevas claves coincidan
    if clave_nueva == clave_actual:
        return jsonify({'status': False, 'data': None, 'message': 'No es posible actualizar por la misma clave'}), 500
    
    #Validar que las nuevas claves coincidan
    if clave_nueva != clave_nueva_confirmada:
        return jsonify({'status': False, 'data': None, 'message': 'Las nuevas claves ingresadas no coinciden'}), 500
    
    #Validar la complejidad de la clave
    valida, mensaje = password_validate(clave_nueva)
    if not valida:
        return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
    
    #Registrar al usuario
    try:
        resultado, mensaje = usuario.actualizar_password(clave_actual, clave_nueva, id)
        if resultado:
            return jsonify({'status': True, 'data': None, 'message': 'Su clave ha sido actualizada correctamenete'}), 200
        else:
            return jsonify({'status': False, 'data': None, 'message': mensaje}), 500
    except Exception as e:
        return jsonify({'status': False, 'data': None, 'message': str(e)}), 500


    