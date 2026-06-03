from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from tools.security import hash_password

class Administrativo:

    def registrar_administrativo(self, data):

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

            # VALIDAR DNI
            sql_dni = """
            SELECT id
            FROM administrativo
            WHERE dni = %s
            """

            cursor.execute(sql_dni, [data['dni']])

            existe_dni = cursor.fetchone()

            if existe_dni:
                return {
                    "error": True,
                    "message": "El DNI ya existe"
                }

            # ENCRIPTAR PASSWORD
            password_hash = hash_password(data['password'])

            # INSERTAR USUARIO
            sql_usuario = """
            INSERT INTO usuario(
                email,
                password,
                rol_id,
                estado_usuario
            )
            VALUES(%s, %s, %s, %s)
            """

            valores_usuario = (
                data['email'],
                password_hash,
                3,  # ADMINISTRATIVO
                'ACTIVO'
            )

            cursor.execute(sql_usuario, valores_usuario)

            usuario_id = cursor.lastrowid

            # INSERTAR ADMINISTRATIVO
            sql_administrativo = """
            INSERT INTO administrativo(
                usuario_id,
                nombres,
                apellidos,
                dni,
                telefono,
                cargo
            )
            VALUES(%s, %s, %s, %s, %s, %s)
            """

            valores_admin = (
                usuario_id,
                data['nombres'],
                data['apellidos'],
                data['dni'],
                data['telefono'],
                data['cargo']
            )

            cursor.execute(sql_administrativo, valores_admin)

            administrativo_id = cursor.lastrowid

            con.commit()

            return {
                "error": False,
                "data": {
                    "usuario_id": usuario_id,
                    "administrativo_id": administrativo_id,
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
            
    
    def listar_administrativos(self):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            a.id AS administrativo_id,
            u.id AS usuario_id,
            u.email,
            a.nombres,
            a.apellidos,
            a.dni,
            a.telefono,
            a.cargo
        FROM administrativo a
        INNER JOIN usuario u
            ON a.usuario_id = u.id
        ORDER BY a.id DESC
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        cursor.close()
        con.close()

        return resultados
    
    
    
    def obtener_administrativo(self, id_administrativo):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            a.id AS administrativo_id,
            u.id AS usuario_id,
            u.email,
            a.nombres,
            a.apellidos,
            a.dni,
            a.telefono,
            a.cargo
        FROM administrativo a
        INNER JOIN usuario u
            ON a.usuario_id = u.id
        WHERE a.id = %s
        """

        cursor.execute(sql, [id_administrativo])

        resultado = cursor.fetchone()

        cursor.close()
        con.close()

        return resultado
    

    def actualizar_administrativo(self, id_administrativo, data):

        con = Conexion().open
        cursor = con.cursor()

        try:

            # VALIDAR EXISTENCIA
            sql_validar = """
            SELECT id
            FROM administrativo
            WHERE id = %s
            """

            cursor.execute(
                sql_validar,
                [id_administrativo]
            )

            existe = cursor.fetchone()

            if not existe:

                return {
                    "error": True,
                    "message": "Administrativo no encontrado"
                }

            # UPDATE
            sql_update = """
            UPDATE administrativo
            SET
                telefono = %s,
                cargo = %s, 
                area = %s
            WHERE id = %s
            """

            valores = (
                data['telefono'],
                data['cargo'],
                data['area'],
                id_administrativo
            )

            cursor.execute(sql_update, valores)

            con.commit()

            return {
                "error": False,
                "data": {
                    "administrativo_id": id_administrativo
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


    def eliminar_administrativo(self, id_administrativo):

        con = Conexion().open
        cursor = con.cursor()

        try:

            # BUSCAR usuario_id
            sql_buscar = """
            SELECT usuario_id
            FROM administrativo
            WHERE id = %s
            """

            cursor.execute(
                sql_buscar,
                [id_administrativo]
            )

            administrativo = cursor.fetchone()

            if not administrativo:

                return {
                    "error": True,
                    "message": "Administrativo no encontrado"
                }

            usuario_id = administrativo['usuario_id']

            # ELIMINAR USUARIO
            sql_delete = """
            DELETE FROM usuario
            WHERE id = %s
            """

            cursor.execute(
                sql_delete,
                [usuario_id]
            )

            con.commit()

            return {
                "error": False,
                "data": {
                    "administrativo_id": id_administrativo
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
