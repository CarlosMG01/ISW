import mysql.connector
import re
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'

mail = Mail(app)



secret_key = '1234' 


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


     # Conexión a la colección 'usuarios'
    
   


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
                    contraseña VARCHAR(255) NOT NULL,
                    imagen_perfil VARCHAR(255)
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
        success = None

        if not correo or not contrasena or not confirmar_contrasena:
            error = 'Correo y contraseña son obligatorios'

        elif contrasena != confirmar_contrasena:
            error = "Las Contraseñas no coinciden"

        elif not re.match(r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+$', correo):
            error = 'Formato de correo incorrecto'
        
       # elif not checkbox:
        #    error = "Es obligatorio aceptar los términos y condiciones"
            
        elif not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,}$', contrasena):
            error = 'La contraseña debe tener al menos 5 caracteres, una mayúscula, una minúscula y un número.'

        else:
            # Verificar si el correo ya está en uso
            query = "SELECT id FROM usuarios WHERE correo = %s"
            self.cursor.execute(query, (correo,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                error = 'Este correo electrónico ya está en uso. Por favor, elige otro.'
            else:
                # El correo no está en uso, proceder con el registro
                success = 'formulario completado'
                # Aquí puedes realizar la inserción en la base de datos si lo deseas
            
        return error, success
    
    def guardar_imagen_perfil(self, correo, imagen_path):
        try:
            query = "UPDATE usuarios SET imagen_perfil = %s WHERE correo = %s"
            self.cursor.execute(query, (imagen_path, correo))
            self.connection.commit()
            return "Imagen de perfil actualizada exitosamente."
        except mysql.connector.Error as err:
            return f"Error al actualizar la imagen de perfil: {err}"
        
    def obtener_imagen_perfil(self, correo):
        try:
            query = "SELECT imagen_perfil FROM usuarios WHERE correo = %s"
            self.cursor.execute(query, (correo,))
            imagen_perfil = self.cursor.fetchone()

            if imagen_perfil:
                return imagen_perfil[0]  # Devuelve la ruta de la imagen de perfil
            else:
                return None  # Si no se encontró una imagen de perfil, devuelve None
        except mysql.connector.Error as err:
            print(f"Error al obtener la imagen de perfil: {err}")
            return None
        
    def change_password(self, correo, contrasena_actual, nueva_contrasena):
        error = None
        success = None

        if not contrasena_actual or not nueva_contrasena:
            error = 'Contraseñas son obligatorios'

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


     

#Funciones para validar correo en el registro



def generar_token(correo):
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps({'correo': correo}, salt='restablecer-contrasena')
    return token

def obtener_correo_desde_token(token):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        data = serializer.loads(token, salt='restablecer-contrasena', max_age=3600)
        correo = data['correo']
        return correo
    except:
        return None

def enviar_correo_verificacion(correo, contrasena):
    token = generar_token(correo)
    url_verificacion = url_for('auth.confirmar_correo', token=token,contrasena =contrasena, _external=True)

    mensaje = Message('Verificación de correo electrónico', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz clic en el siguiente enlace para verificar tu correo electrónico: {url_verificacion}'

    mail.send(mensaje)

def confirmar_correo_en_bd(correo, contrasena, cursor, connection):
    query = "INSERT INTO usuarios (correo, contraseña) VALUES (%s, %s)"
    values = (correo, contrasena)
    cursor.execute(query, values)
    connection.commit()

def verificar_credenciales_en_bd(correo, contrasena, cursor):
    query = "SELECT id FROM usuarios WHERE correo = ? AND contraseña = ?"
    cursor.execute(query, (correo, contrasena))
    user_id = cursor.fetchone()
    return user_id

def enviar_correo_restablecer(correo):
    token = generar_token(correo)
    url_restablecer = url_for('auth.olvide_contrasena', token=token, _external=True)

    mensaje = Message('Restablecimiento de contraseña', sender='ceupractica@gmail.com', recipients=[correo])
    mensaje.body = f'Haz click en el siguiente enlace para restablecer tu contraseña: ´{url_restablecer}'

    mail.send(mensaje)

##################################################################################################################3


def login(correo, contrasena, cursor):
    error = None

    if not correo or not contrasena:
        error = "Correo y contraseña son obligatorios"
    else:
        try:
            query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            values = (correo, contrasena)
            cursor.execute(query, values)
            user = cursor.fetchone()
            if user is not None:
                return True, None  # Éxito en el inicio de sesión, sin errores
            else:
                error = "Credenciales incorrectas"
        except mysql.connector.Error as err:
            error = f"Error al realizar la consulta en la base de datos: {err}"

    return False, error


db = BaseDeDatosMariaDB()
db.conectar()
