from conexionBD import Conexion

class Cita:

    def registrar_cita(self, data):

        #Abri conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()

        try:

            # VALIDAR PACIENTE
            sql_paciente = """
            SELECT id
            FROM paciente
            WHERE id = %s
            """

            cursor.execute(
                sql_paciente,
                [data['paciente_id']]
            )

            paciente = cursor.fetchone()

            if not paciente:

                return {
                    "error": True,
                    "message": "El paciente no existe"
                }

            # VALIDAR HORARIO
            sql_horario = """
            SELECT
                id,
                estado_horario_disponible_id
            FROM horario_disponible
            WHERE id = %s
            """

            cursor.execute(
                sql_horario,
                [data['horario_disponible_id']]
            )

            horario = cursor.fetchone()

            if not horario:

                return {
                    "error": True,
                    "message": "El horario no existe"
                }

            # VALIDAR DISPONIBILIDAD
            if horario['estado_horario_disponible_id'] != 1:

                return {
                    "error": True,
                    "message": "El horario no está disponible"
                }

            # VALIDAR USUARIO
            sql_usuario = """
            SELECT id
            FROM usuario
            WHERE id = %s
            """

            cursor.execute(
                sql_usuario,
                [data['creado_por_usuario_id']]
            )

            usuario = cursor.fetchone()

            if not usuario:

                return {
                    "error": True,
                    "message": "El usuario creador no existe"
                }

            # INSERTAR CITA
            sql_insert = """
            INSERT INTO cita(
                paciente_id,
                horario_disponible_id,
                motivo,
                paciente_oncologico,
                estado_cita_id,
                creado_por_usuario_id
            )
            VALUES(%s, %s, %s, %s, %s, %s)
            """

            valores = (
                data['paciente_id'],
                data['horario_disponible_id'],
                data['motivo'],
                data['paciente_oncologico'],
                1, # PENDIENTE
                data['creado_por_usuario_id']
            )

            cursor.execute(sql_insert, valores)

            cita_id = cursor.lastrowid

            # ACTUALIZAR HORARIO A RESERVADO
            sql_update = """
            UPDATE horario_disponible
            SET estado_horario_disponible_id = 2
            WHERE id = %s
            """

            cursor.execute(
                sql_update,
                [data['horario_disponible_id']]
            )

            con.commit()

            return {
                "error": False,
                "data": {
                    "cita_id": cita_id
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
            
            
    def listar_citas_paciente(self, id_paciente):
        #Abri conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        try:

            # VALIDAR PACIENTE
            sql_paciente = """
            SELECT id
            FROM paciente
            WHERE id = %s
            """

            cursor.execute(
                sql_paciente,
                [id_paciente]
            )

            paciente = cursor.fetchone()

            if not paciente:

                return {
                    "error": True,
                    "message": "El paciente no existe"
                }

            # LISTAR CITAS
            sql = """
            SELECT

                c.id AS cita_id,
                c.motivo,
                c.paciente_oncologico,
                c.fecha_registro,

                hd.fecha,
                hd.hora_inicio,
                hd.hora_fin,

                m.id AS medico_id,

                CONCAT(
                    m.nombres,
                    ' ',
                    m.apellidos
                ) AS medico,

                e.id AS especialidad_id,
                e.nombre AS especialidad,

                ec.nombre AS estado_cita

            FROM cita c

            INNER JOIN horario_disponible hd
                ON c.horario_disponible_id = hd.id

            INNER JOIN medico m
                ON hd.medico_id = m.id

            INNER JOIN especialidad e
                ON hd.especialidad_id = e.id

            INNER JOIN estado_cita ec
                ON c.estado_cita_id = ec.id

            WHERE c.paciente_id = %s

            ORDER BY hd.fecha DESC,
                    hd.hora_inicio DESC
            """

            cursor.execute(sql, [id_paciente])

            resultados = cursor.fetchall()

            return {
                "error": False,
                "data": resultados
            }

        except Exception as e:

            return {
                "error": True,
                "message": str(e)
            }

        finally:

            cursor.close()
            con.close()
            
            
    def cancelar_cita(self, id_cita):

        #Abri conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()

        try:

            # VALIDAR EXISTENCIA DE LA CITA
            sql_cita = """
            SELECT
                id,
                horario_disponible_id,
                estado_cita_id
            FROM cita
            WHERE id = %s
            """

            cursor.execute(
                sql_cita,
                [id_cita]
            )

            cita = cursor.fetchone()

            if not cita:

                return {
                    "error": True,
                    "message": "La cita no existe"
                }

            # VALIDAR SI YA ESTÁ CANCELADA
            if cita['estado_cita_id'] == 3:

                return {
                    "error": True,
                    "message": "La cita ya está cancelada"
                }

            # ACTUALIZAR ESTADO CITA
            sql_update_cita = """
            UPDATE cita
            SET estado_cita_id = 3
            WHERE id = %s
            """

            cursor.execute(
                sql_update_cita,
                [id_cita]
            )

            # LIBERAR HORARIO
            sql_update_horario = """
            UPDATE horario_disponible
            SET estado_horario_disponible_id = 1
            WHERE id = %s
            """

            cursor.execute(
                sql_update_horario,
                [cita['horario_disponible_id']]
            )

            con.commit()

            return {
                "error": False,
                "data": {
                    "cita_id": id_cita
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
            
            
    def listar_citas_medico(self, id_medico):

        #Abri conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
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
                [id_medico]
            )

            medico = cursor.fetchone()

            if not medico:

                return {
                    "error": True,
                    "message": "El médico no existe"
                }

            # LISTAR CITAS
            sql = """
            SELECT

                c.id AS cita_id,

                p.id AS paciente_id,

                CONCAT(
                    p.nombres,
                    ' ',
                    p.apellidos
                ) AS paciente,

                c.motivo,
                c.paciente_oncologico,

                hd.fecha,
                hd.hora_inicio,
                hd.hora_fin,

                e.id AS especialidad_id,
                e.nombre AS especialidad,

                ec.nombre AS estado_cita,

                c.fecha_registro

            FROM cita c

            INNER JOIN paciente p
                ON c.paciente_id = p.id

            INNER JOIN horario_disponible hd
                ON c.horario_disponible_id = hd.id

            INNER JOIN especialidad e
                ON hd.especialidad_id = e.id

            INNER JOIN estado_cita ec
                ON c.estado_cita_id = ec.id

            WHERE hd.medico_id = %s

            ORDER BY hd.fecha DESC,
                    hd.hora_inicio DESC
            """

            cursor.execute(sql, [id_medico])

            resultados = cursor.fetchall()

            return {
                "error": False,
                "data": resultados
            }

        except Exception as e:

            return {
                "error": True,
                "message": str(e)
            }

        finally:

            cursor.close()
            con.close()