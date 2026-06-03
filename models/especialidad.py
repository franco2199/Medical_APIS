from conexionBD import Conexion

class Especialidad:

    def registrar_especialidad(self, data):

        #Abrir la conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # VALIDAR NOMBRE DUPLICADO
            sql_validar = """
            SELECT id
            FROM especialidad
            WHERE nombre = %s
            """

            cursor.execute(
                sql_validar,
                [data['nombre']]
            )

            existe = cursor.fetchone()

            if existe:

                return {
                    "error": True,
                    "message": "La especialidad ya existe"
                }

            # INSERTAR
            sql_insert = """
            INSERT INTO especialidad(
                nombre,
                descripcion
            )
            VALUES(%s, %s)
            """

            valores = (
                data['nombre'],
                data['descripcion']
            )

            cursor.execute(sql_insert, valores)

            especialidad_id = cursor.lastrowid

            con.commit()

            return {
                "error": False,
                "data": {
                    "especialidad_id": especialidad_id,
                    "nombre": data['nombre']
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
            
            
    def listar_especialidades(self):

        #Abrir la conexión
        con = Conexion().open
            
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            id AS especialidad_id,
            nombre,
            descripcion
        FROM especialidad
        ORDER BY id DESC
        """

        cursor.execute(sql)

        resultados = cursor.fetchall()

        cursor.close()
        con.close()

        return resultados
    
    
    
    def obtener_especialidad(self, id_especialidad):

        #Abrir la conexión
        con = Conexion().open
            
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        sql = """
        SELECT
            id AS especialidad_id,
            nombre,
            descripcion
        FROM especialidad
        WHERE id = %s
        """

        cursor.execute(sql, [id_especialidad])

        resultado = cursor.fetchone()

        cursor.close()
        con.close()

        return resultado
    
    
    def actualizar_especialidad(self, id_especialidad, data):

        #Abrir la conexión
        con = Conexion().open
            
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # VALIDAR EXISTENCIA
            sql_validar = """
            SELECT id
            FROM especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_validar,
                [id_especialidad]
            )

            existe = cursor.fetchone()

            if not existe:

                return {
                    "error": True,
                    "message": "Especialidad no encontrada"
                }

            # VALIDAR NOMBRE DUPLICADO
            sql_nombre = """
            SELECT id
            FROM especialidad
            WHERE nombre = %s
            AND id <> %s
            """

            cursor.execute(
                sql_nombre,
                (
                    data['nombre'],
                    id_especialidad
                )
            )

            nombre_existe = cursor.fetchone()

            if nombre_existe:

                return {
                    "error": True,
                    "message": "El nombre de la especialidad ya existe"
                }

            # UPDATE
            sql_update = """
            UPDATE especialidad
            SET
                nombre = %s,
                descripcion = %s
            WHERE id = %s
            """

            valores = (
                data['nombre'],
                data['descripcion'],
                id_especialidad
            )

            cursor.execute(sql_update, valores)

            con.commit()

            return {
                "error": False,
                "data": {
                    "especialidad_id": id_especialidad
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
            
            
    def eliminar_especialidad(self, id_especialidad):

        #Abrir la conexión
        con = Conexion().open
            
        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        try:

            # VALIDAR EXISTENCIA
            sql_validar = """
            SELECT id
            FROM especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_validar,
                [id_especialidad]
            )

            existe = cursor.fetchone()

            if not existe:

                return {
                    "error": True,
                    "message": "Especialidad no encontrada"
                }

            # DELETE
            sql_delete = """
            DELETE FROM especialidad
            WHERE id = %s
            """

            cursor.execute(
                sql_delete,
                [id_especialidad]
            )

            con.commit()

            return {
                "error": False,
                "data": {
                    "especialidad_id": id_especialidad
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