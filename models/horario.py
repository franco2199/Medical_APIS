from conexionBD import Conexion

class Horario:

    def horario_disponibles(self, data):

        #Abri conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()

        try:

            sql = """
            SELECT

                hd.id AS horario_disponible_id,

                m.id AS medico_id,

                CONCAT(
                    m.nombres,
                    ' ',
                    m.apellidos
                ) AS medico,

                e.id AS especialidad_id,
                e.nombre AS especialidad,

                hd.fecha,
                hd.hora_inicio,
                hd.hora_fin,

                ehd.nombre AS estado

            FROM horario_disponible hd

            INNER JOIN medico m
                ON hd.medico_id = m.id

            INNER JOIN especialidad e
                ON hd.especialidad_id = e.id

            INNER JOIN estado_horario_disponible ehd
                ON hd.estado_horario_disponible_id = ehd.id

            WHERE hd.especialidad_id = %s
            AND hd.fecha = %s
            AND hd.estado_horario_disponible_id = 1

            ORDER BY hd.hora_inicio ASC
            """

            cursor.execute(
                sql,
                (
                    data['especialidad_id'],
                    data['fecha']
                )
            )

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