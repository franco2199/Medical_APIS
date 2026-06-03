from conexionBD import Conexion
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class Usuario: 
    def __init__(self):
        self.ph = PasswordHasher()
        
    def login(self, email, clave):
        #Abri conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = """
           SELECT 
        u.id AS usuario_id,
        u.email,
        r.nombre AS rol,
        eu.nombre AS estado_usuario,
        COALESCE(p.nombres, m.nombres, a.nombres) AS nombres,
        COALESCE(p.apellidos, m.apellidos, a.apellidos) AS apellidos, 
        u.password AS clave
        FROM usuario u
        INNER JOIN rol r 
            ON u.rol_id = r.id
        INNER JOIN estado_usuario eu 
            ON u.estado_usuario_id = eu.id
        LEFT JOIN paciente p 
            ON u.id = p.usuario_id
        LEFT JOIN medico m 
            ON u.id = m.usuario_id
        LEFT JOIN administrativo a 
            ON u.id = a.usuario_id
        WHERE u.email = %s

            """
        
        #Ejeutar la sentencia SQL
        cursor.execute (sql, [email])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        #Verificar si se encontró el usuario con el email ingresado
        if resultado:
            try:
                #Validar la clave almacenada en la bd con la que ingresa el usuario
                self.ph.verify(resultado['clave'], clave) #ojo
                return resultado
            except VerifyMismatchError:
                return None    
            
        else: #No se encontro ningún registro con el email ingresado
            return None

    
    def obtener_foto(self, usuario_id):
        #Abri conexión
        con = Conexion().open
    
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
    
        #Definir la sentencia SQL
        sql = """
        SELECT coalesce(foto, 'x') as foto from usuario where id = %s

            """
        #Ejeutar la sentencia SQL
        cursor.execute (sql, [usuario_id])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        #Verificar si se encontro la foto del usuario
        if resultado and resultado['foto'] != 'x':
            return resultado
        else: #No se encoentro la fot
            return None
        
        
        
    def obtener_perfil(self, usuario_id): 
         #Abri conexión
        con = Conexion().open
        
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
        
        #Definir la sentencia SQL
        sql = """
           SELECT 
    u.id AS usuario_id,
    u.email,
    r.nombre AS rol,
    COALESCE(p.nombres, m.nombres, a.nombres) AS nombres,
    COALESCE(p.apellidos, m.apellidos, a.apellidos) AS apellidos
    FROM usuario u
    INNER JOIN rol r 
        ON u.rol_id = r.id
    INNER JOIN estado_usuario eu 
        ON u.estado_usuario_id = eu.id
    LEFT JOIN paciente p 
        ON u.id = p.usuario_id
    LEFT JOIN medico m 
        ON u.id = m.usuario_id
    LEFT JOIN administrativo a 
        ON u.id = a.usuario_id
    WHERE u.id = %s

            """
            
        #Ejeutar la sentencia SQL
        cursor.execute (sql, [usuario_id])
        
        #Recuperar los datos del usuario
        resultado = cursor.fetchone()
        
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        return resultado
    
    def actualizar_foto(self, foto, id): 
        #Abri conexión
        con = Conexion().open
            
        #Crear un cursor para ejecutar una sentencia SQL
        cursor = con.cursor()
            
        #Definir la sentencia SQL
        sql = """
            UPDATE usuario SET foto=%s
            WHERE id = %s    
            """
        
        #Ejeutar la sentencia SQL
        cursor.execute (sql, [foto, id])
        
        #Confirmar los datos en la BD
        con.commit()
            
        #Cerrar el cursor y la conexión
        cursor.close()
        con.close()
        
        #Retonar al final true
        return True, 'ok'   

    def actualizar_password(self, clave_actual, clave_nueva, id):
        #Abrir la conexión
        con = Conexion().open

        #Crear un cursor para ejecutar la sentencia sql
        cursor = con.cursor()

        #Definir la sentencia sql para validar el dni e email
        sql_validar = "SELECT password FROM usuario WHERE id=%s"

        #Ejecutar la sentencia
        cursor.execute(sql_validar,[id])

        #Recuperar los datos del usuario
        resultado = cursor.fetchone()

        #Validar que la clave sea correcta
        try:
            self.ph.verify(resultado['password'], clave_actual)    
        except VerifyMismatchError:
            return False, 'La clave actual es incorrecta, verifique'

        #Definir la sentencia sql
        sql = """
        UPDATE 
        usuario 
        set 
        password = %s
        where
        id = %s
        """

        #Ejecutar la sentencia
        cursor.execute(sql,[ self.ph.hash(clave_nueva), id])

        #Confirmar los datos en la BD
        con.commit()

        #Cerrar el curso y la conexión
        cursor.close()
        con.close()

        #Retonar al final true
        return True, 'ok'    
    
    


    


