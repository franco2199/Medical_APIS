from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class MedicoEspecialidad:

    def registrar_relacion(self, data):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # VALIDAR MÉDICO
            sql_medico = """
            SELECT id
            FROM medico
            WHERE id = %s
            """

            cursor.execute(
                sql_medico,
                [data['medico_id']]
            )

            existe_medico = cursor.fetchone()

            if not existe_medico:

                return {
                    "error": True,
                    "message": "El médico no existe"
                }

            # VALIDAR ESPECIALIDAD
            sql_especialidad = """
            SELECT id
            FROM especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_especialidad,
                [data['especialidad_id']]
            )

            existe_especialidad = cursor.fetchone()

            if not existe_especialidad:

                return {
                    "error": True,
                    "message": "La especialidad no existe"
                }

            # VALIDAR DUPLICADO
            sql_duplicado = """
            SELECT id
            FROM medico_especialidad
            WHERE medico_id = %s
            AND especialidad_id = %s
            """

            cursor.execute(
                sql_duplicado,
                (
                    data['medico_id'],
                    data['especialidad_id']
                )
            )

            existe_relacion = cursor.fetchone()

            if existe_relacion:

                return {
                    "error": True,
                    "message": "La relación ya existe"
                }

            # INSERTAR
            sql_insert = """
            INSERT INTO medico_especialidad(
                medico_id,
                especialidad_id
            )
            VALUES(%s, %s)
            """

            valores = (
                data['medico_id'],
                data['especialidad_id']
            )

            cursor.execute(sql_insert, valores)

            relacion_id = cursor.lastrowid

            con.commit()

            return {
                "error": False,
                "data": {
                    "medico_especialidad_id": relacion_id,
                    "medico_id": data['medico_id'],
                    "especialidad_id": data['especialidad_id']
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
            
    def listar_relaciones(self):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            me.id AS medico_especialidad_id,

            m.id AS medico_id,

            CONCAT(
                m.nombres,
                ' ',
                m.apellidos
            ) AS medico,

            e.id AS especialidad_id,
            e.nombre AS especialidad

        FROM medico_especialidad me

        INNER JOIN medico m
            ON me.medico_id = m.id

        INNER JOIN especialidad e
            ON me.especialidad_id = e.id

        ORDER BY me.id DESC
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        cursor.close()
        con.close()

        return resultados
    
    
    def obtener_relacion(self, id_relacion):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            me.id AS medico_especialidad_id,

            m.id AS medico_id,

            CONCAT(
                m.nombres,
                ' ',
                m.apellidos
            ) AS medico,

            e.id AS especialidad_id,
            e.nombre AS especialidad

        FROM medico_especialidad me

        INNER JOIN medico m
            ON me.medico_id = m.id

        INNER JOIN especialidad e
            ON me.especialidad_id = e.id

        WHERE me.id = %s
        """

        cursor.execute(sql, [id_relacion])

        resultado = cursor.fetchone()

        cursor.close()
        con.close()

        return resultado
    
    
    def actualizar_relacion(self, id_relacion, data):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # VALIDAR RELACIÓN
            sql_relacion = """
            SELECT id
            FROM medico_especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_relacion,
                [id_relacion]
            )

            existe_relacion = cursor.fetchone()

            if not existe_relacion:

                return {
                    "error": True,
                    "message": "Relación no encontrada"
                }

            # VALIDAR MÉDICO
            sql_medico = """
            SELECT id
            FROM medico
            WHERE id = %s
            """

            cursor.execute(
                sql_medico,
                [data['medico_id']]
            )

            existe_medico = cursor.fetchone()

            if not existe_medico:

                return {
                    "error": True,
                    "message": "El médico no existe"
                }

            # VALIDAR ESPECIALIDAD
            sql_especialidad = """
            SELECT id
            FROM especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_especialidad,
                [data['especialidad_id']]
            )

            existe_especialidad = cursor.fetchone()

            if not existe_especialidad:

                return {
                    "error": True,
                    "message": "La especialidad no existe"
                }

            # VALIDAR DUPLICADO
            sql_duplicado = """
            SELECT id
            FROM medico_especialidad
            WHERE medico_id = %s
            AND especialidad_id = %s
            AND id <> %s
            """

            cursor.execute(
                sql_duplicado,
                (
                    data['medico_id'],
                    data['especialidad_id'],
                    id_relacion
                )
            )

            duplicado = cursor.fetchone()

            if duplicado:

                return {
                    "error": True,
                    "message": "La relación ya existe"
                }

            # UPDATE
            sql_update = """
            UPDATE medico_especialidad
            SET
                medico_id = %s,
                especialidad_id = %s
            WHERE id = %s
            """

            valores = (
                data['medico_id'],
                data['especialidad_id'],
                id_relacion
            )

            cursor.execute(sql_update, valores)

            con.commit()

            return {
                "error": False,
                "data": {
                    "medico_especialidad_id": id_relacion
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
            
            
    def eliminar_relacion(self, id_relacion):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()
        
        
        try:

            # VALIDAR EXISTENCIA
            sql_validar = """
            SELECT id
            FROM medico_especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_validar,
                [id_relacion]
            )

            existe = cursor.fetchone()

            if not existe:

                return {
                    "error": True,
                    "message": "Relación no encontrada"
                }

            # DELETE
            sql_delete = """
            DELETE FROM medico_especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_delete,
                [id_relacion]
            )

            con.commit()

            return {
                "error": False,
                "data": {
                    "medico_especialidad_id": id_relacion
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