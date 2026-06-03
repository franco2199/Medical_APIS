from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Paciente: 
    def registrar_paciente(self, usuario_id,nombres, apellidos, dni, celular, genero):
        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        #Definir la sentencia sql para validar el dni e email
        sql = "SELECT id FROM paciente WHERE dni=%s"
        
        #Ejecutar la sentencia
        cursor.execute(sql,[dni])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Validar dni o email duplicado
        if resultado:
            return False, 'El DNI ingresado ya se encuentra registrado por otro usuario'
        
        #Definir la sentencia sql
        sql = """
            INSERT INTO paciente (usuario_id, nombres, apellidos, dni, celular, genero) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        
        #Ejecutar la sentencia
        cursor.execute(sql,[usuario_id, nombres, apellidos, dni, celular, genero])
        
        #Confirmar los datos en la BD
        con.commit()
        
        #Cerrar el curso y la conexión
        cursor.close()
        con.close()
        
        #Retonar al final true
        return True, 'ok'
    

    def listar_pacientes(self):

       #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            p.id AS paciente_id,
            u.id AS usuario_id,
            u.email,
            p.nombres,
            p.apellidos,
            p.dni,
            p.celular
        FROM paciente p
        INNER JOIN usuario u
            ON p.usuario_id = u.id
        ORDER BY p.id DESC
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        cursor.close()
        con.close()

        return resultados
    

    def obtener_paciente(self, id_paciente):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            p.id AS paciente_id,
            u.id AS usuario_id,
            u.email,
            p.nombres,
            p.apellidos,
            p.dni,
            p.celular,
            p.fecha_nacimiento,
            p.genero
        FROM paciente p
        INNER JOIN usuario u
            ON p.usuario_id = u.id
        WHERE p.id = %s
        """

        cursor.execute(sql, [id_paciente])

        resultado = cursor.fetchone()

        cursor.close()
        con.close()

        return resultado
    
    
    def actualizar_paciente(self, id_paciente, data):

        con = Conexion().open
        cursor = con.cursor()

        try:

            # VALIDAR EXISTENCIA
            sql = """
            SELECT id
            FROM paciente
            WHERE id = %s
            """

            cursor.execute(sql, [id_paciente])

            existe = cursor.fetchone()

            if not existe:
                return {
                    "error": True,
                    "message": "Paciente no encontrado"
                }

            # UPDATE
            sql = """
            UPDATE paciente
            SET
                nombres = %s,
                apellidos = %s,
                celular = %s,
                fecha_nacimiento = %s,
                genero = %s
            WHERE id = %s
            """

            valores = (
                data['nombres'],
                data['apellidos'],
                data['celular'],
                data['fecha_nacimiento'],
                data['genero'],
                id_paciente
            )

            cursor.execute(sql, valores)

            con.commit()

            return {
                "error": False,
                "data": {
                    "paciente_id": id_paciente
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
            
    
    def eliminar_paciente(self, id_paciente):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # OBTENER usuario_id
            sql_buscar = """
            SELECT usuario_id
            FROM paciente
            WHERE id = %s
            """

            cursor.execute(sql_buscar, [id_paciente])

            paciente = cursor.fetchone()

            if not paciente:
                return {
                    "error": True,
                    "message": "Paciente no encontrado"
                }

            usuario_id = paciente['usuario_id']

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
                    "paciente_id": id_paciente
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