from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from tools.security import hash_password


class Medico:

    def registrar_medico(self, data):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # VALIDAR EMAIL
            sql_email = """
            SELECT id
            FROM usuario
            WHERE email = %s
            """

            cursor.execute(sql_email, [data['email']])

            existe_email = cursor.fetchone()

            if existe_email:
                return {
                    "error": True,
                    "message": "El email ya existe"
                }

            # VALIDAR CMP
            sql_cmp = """
            SELECT id
            FROM medico
            WHERE cmp = %s
            """

            cursor.execute(sql_cmp, [data['cmp']])

            existe_cmp = cursor.fetchone()

            if existe_cmp:
                return {
                    "error": True,
                    "message": "El CMP ya existe"
                }

            # ENCRIPTAR PASSWORD
            password_hash = hash_password(data['password'])

            # INSERTAR USUARIO
            sql_usuario = """
            INSERT INTO usuario(
                email,
                password,
                rol_id,
                estado_usuario, foto
            )
            VALUES(%s, %s, %s, %s, %s)
            """

            valores_usuario = (
                data['email'],
                password_hash,
                2,  # MEDICO
                'ACTIVO'
            )

            cursor.execute(sql_usuario, valores_usuario)

            usuario_id = cursor.lastrowid

            # INSERTAR MEDICO
            sql_medico = """
            INSERT INTO medico(
                usuario_id,
                nombres,
                apellidos,
                dni,
                cmp,
                telefono,
                consultorio,
                estado_medico_id
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores_medico = (
                usuario_id,
                data['nombres'],
                data['apellidos'],
                data['dni'],
                data['cmp'],
                data['telefono'],
                data['consultorio'],
                data['estado_medico_id']
            )

            cursor.execute(sql_medico, valores_medico)

            medico_id = cursor.lastrowid

            con.commit()

            return {
                "error": False,
                "data": {
                    "usuario_id": usuario_id,
                    "medico_id": medico_id,
                    "email": data['email']
                }
            }

        except Exception as e:

            con.rollback()

            return {
                "error": True,
                "message": str(e)
            }

        finally:

            cursor.close()
            con.close()
            
    
    def listar_medicos(self):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            m.id AS medico_id,
            u.id AS usuario_id,
            u.email,
            m.nombres,
            m.apellidos,
            m.cmp,
            m.consultorio
        FROM medico m
        INNER JOIN usuario u
            ON m.usuario_id = u.id
        ORDER BY m.id DESC
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        cursor.close()
        con.close()

        return resultados
    
    
    def obtener_medico(self, id_medico):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            m.id AS medico_id,
            u.id AS usuario_id,
            u.email,
            m.nombres,
            m.apellidos,
            m.dni,
            m.cmp,
            m.telefono,
            m.consultorio,
            em.nombre AS estado_medico
        FROM medico m
        INNER JOIN usuario u
            ON m.usuario_id = u.id
        INNER JOIN estado_medico em
            ON m.estado_medico_id = em.id
        WHERE m.id = %s
        """

        cursor.execute(sql, [id_medico])

        resultado = cursor.fetchone()

        cursor.close()
        con.close()

        return resultado
    
    
    def actualizar_medico(self, id_medico, data):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # VALIDAR EXISTENCIA
            sql_validar = """
            SELECT id
            FROM medico
            WHERE id = %s
            """

            cursor.execute(sql_validar, [id_medico])

            existe = cursor.fetchone()

            if not existe:
                return {
                    "error": True,
                    "message": "Médico no encontrado"
                }

            # VALIDAR estado_medico_id
            sql_estado = """
            SELECT id
            FROM estado_medico
            WHERE id = %s
            """

            cursor.execute(sql_estado, [data['estado_medico_id']])

            existe_estado = cursor.fetchone()

            if not existe_estado:
                return {
                    "error": True,
                    "message": "Estado médico inválido"
                }

            # UPDATE
            sql_update = """
            UPDATE medico
            SET
                telefono = %s,
                consultorio = %s,
                estado_medico_id = %s
            WHERE id = %s
            """

            valores = (
                data['telefono'],
                data['consultorio'],
                data['estado_medico_id'],
                id_medico
            )

            cursor.execute(sql_update, valores)

            con.commit()

            return {
                "error": False,
                "data": {
                    "medico_id": id_medico
                }
            }

        except Exception as e:

            con.rollback()

            return {
                "error": True,
                "message": str(e)
            }

        finally:

            cursor.close()
            con.close()
            
            
    def eliminar_medico(self, id_medico):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # BUSCAR usuario_id
            sql_buscar = """
            SELECT usuario_id
            FROM medico
            WHERE id = %s
            """

            cursor.execute(sql_buscar, [id_medico])

            medico = cursor.fetchone()

            if not medico:
                return {
                    "error": True,
                    "message": "Médico no encontrado"
                }

            usuario_id = medico['usuario_id']

            # ELIMINAR USUARIO
            sql_delete = """
            DELETE FROM usuario
            WHERE id = %s
            """

            cursor.execute(sql_delete, [usuario_id])

            con.commit()

            return {
                "error": False,
                "data": {
                    "medico_id": id_medico
                }
            }

        except Exception as e:

            con.rollback()

            return {
                "error": True,
                "message": str(e)
            }

        finally:

            cursor.close()
            con.close()