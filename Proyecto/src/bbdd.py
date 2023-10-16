import mysql.connector
import re

class BaseDeDatosMariaDB:
    def __init__(self):
        self.host = "localhost"
        self.usuario = "root"
        self.contraseña = "root"
        self.base_de_datos = "prueba"
        self.conexion = None

    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(
                host=self.host,
                user=self.usuario,
                password=self.contraseña,
                database=self.base_de_datos
            )
            print("Conexión a la base de datos exitosa.")
            self.crear_tablas()  # Llamar a la función para crear tablas
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")

    def desconectar(self):
        if self.conexion is not None and self.conexion.is_connected():
            self.conexion.close()
            print("Desconexión de la base de datos exitosa.")

    def crear_tablas(self):
        try:
            cursor = self.conexion.cursor()
            # Crear la tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    correo VARCHAR(255) NOT NULL,
                    contraseña VARCHAR(255) NOT NULL
                )
            """)

            # Crear la tabla de textos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS textos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT,
                    titulo VARCHAR(255) NOT NULL,
                    contenido TEXT NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            """)

            print("Tablas creadas correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al crear las tablas: {err}")


class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def register_user(self, correo, contrasena, confirmar_contrasena):
        error = None  
        success= None

        if not correo or not contrasena or not confirmar_contrasena:
            error = 'Correo y contraseña son obligatorios'

        elif contrasena != confirmar_contrasena:
            error = "Las Contraseñas no coinciden"

        elif not re.match(r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+$', correo):
            error = 'Formato de correo incorrecto'

        elif not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,}$', contrasena):
            error = 'La contraseña debe tener al menos 5 caracteres, una mayúscula, una minúscula y un número.'
        
        else:
            try:
                query = "SELECT id FROM usuarios WHERE correo = %s"
                self.cursor.execute(query, (correo,))
                existing_user = self.cursor.fetchone()

                if existing_user:
                    error = 'Correo ya registrado, por favor use otro correo.'

                else:
                    query = "INSERT INTO usuarios (correo, contraseña) VALUES (%s, %s)"
                    values = (correo, contrasena)
                    self.cursor.execute(query, values)
                    self.connection.commit()
                    success='Correo de confirmación enviado'

            except mysql.connector.Error as err:
                error = f'Error al registrar usuario: {err}'

        return error, success
     
     






    def login(self, correo, contrasena):
        error = None

        if not correo or not contrasena:
            error = "Correo y contraseña son obligatorios"
        else:
            try:
                query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
                values = (correo, contrasena)
                self.cursor.execute(query, values)
                user = self.cursor.fetchone()
                if user is not None:
                    return True, None  # Éxito en el inicio de sesión, sin errores
                else:
                    error = "Credenciales incorrectas"
            except mysql.connector.Error as err:
                error = f"Error al realizar la consulta en la base de datos: {err}"

        return False, error
    
    def change_password(self, correo, contrasena_actual, nueva_contrasena):
        error = None
        success = None

        if not correo or not contrasena_actual or not nueva_contrasena:
            error = 'Correo y contraseñas son obligatorios'

        else:
            try:
                query = "SELECT id FROM usuarios WHERE correo = %s AND contraseña = %s"
                self.cursor.execute(query, (correo, contrasena_actual))
                user_id = self.cursor.fetchone()

                if user_id is not None:
                    query = "UPDATE usuarios SET contraseña = %s WHERE id = %s"
                    self.cursor.execute(query, (nueva_contrasena, user_id[0]))
                    self.connection.commit()
                    success = 'Contraseña actualizada exitosamente'
                else:
                    error = 'Credenciales incorrectas'
            except mysql.connector.Error as err:
                error = f'Error al cambiar la contraseña: {err}'

        return error, success

    

    
db = BaseDeDatosMariaDB()
db.conectar()
