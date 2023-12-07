import mysql.connector
import re
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from flask_mail import Mail, Message
from flask import Flask
from PIL import Image
import io
import base64

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'

mail = Mail(app)


# Cargar la imagen desde el disco

secret_key = '1234' 


class BaseDeDatosMariaDB:
    def __init__(self):
        self.host = "localhost"
        self.usuario = "carlos"
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
            query = """CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    correo VARCHAR(255) NOT NULL,
                    contraseña VARCHAR(255) NOT NULL,
                    imagen_perfil LONGBLOB  
                )"""
            cursor.execute(query)

            # Crear la tabla de textos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS textos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT,
                    titulo VARCHAR(255) NOT NULL,
                    contenido TEXT NOT NULL
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
            # Cargar la imagen desde el disco
            with Image.open(imagen_path) as imagen:
                # Obtener los datos binarios de la imagen
                with io.BytesIO() as output:
                    imagen.save(output, format=imagen.format)  # Guardar en el mismo formato original
                    datos_binarios = output.getvalue()
            query = "UPDATE usuarios SET imagen_perfil = %s WHERE correo = %s"
            self.cursor.execute(query, (datos_binarios,correo))
            self.connection.commit()
            return "Imagen de perfil actualizada exitosamente."
        except mysql.connector.Error as err:
            return f"Error al actualizar la imagen de perfil: {err}"
        
    def obtener_imagen_perfil(self, correo):
        try:
            query = "SELECT imagen_perfil FROM usuarios WHERE correo = %s"
            self.cursor.execute(query, (correo,))
            imagen_perfil = self.cursor.fetchone()

            if imagen_perfil[0] is not None:
                imagen = imagen_perfil[0]
                datos_binarios_procesados = base64.b64encode(imagen).decode('utf-8')
                return datos_binarios_procesados

            else:
                with Image.open("static/perfil.png") as imagen:
                        # Obtener los datos binarios de la imagen
                    with io.BytesIO() as output:
                        imagen.save(output, format=imagen.format)  # Guardar en el mismo formato original
                        datos_binarios = output.getvalue()
                        datos_binarios_procesados = base64.b64encode(datos_binarios).decode('utf-8')
                return datos_binarios_procesados
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
    
    def verificar_usuario_por_correo(self, correo):
        error = None
        success = None
        query = "SELECT id FROM usuarios WHERE correo = %s"
        self.cursor.execute(query, (correo,))
        comprobacion = self.cursor.fetchone()
        if comprobacion is not None:
            success = 'Se ha enviado un correo electrónico con la contraseña'
        else:
            error = 'Correo electrónico no registrado en la página web'
        return error, success;

    def restablecer_contrasena(self, correo, nueva_contrasena):
        error = None
        success = None

        if not nueva_contrasena:
            error = 'Contraseñas son obligatorios'

        else:
            query = "UPDATE usuarios SET contraseña = %s WHERE correo = %s"
            try:
                self.cursor.execute(query, (nueva_contrasena, correo))
                self.connection.commit()
                success = "Contraseña restablecida correctamente"
            except mysql.connector.Error as err:
                error = f'Error al cambiar la contraseña: {err}'

        return error, success

    def guardar_documento(self, usuario_id, titulo, contenido):
        try:
            query = "INSERT INTO textos (usuario_id, titulo, contenido) VALUES (%s, %s, %s)"
            values = (usuario_id, titulo, contenido)
            self.cursor.execute(query, values)
            self.connection.commit()

            return "Documento guardado correctamente."
        except mysql.connector.Error as err:
            return f"Error al guardar el documento: {err}"


    def obtener_documentos(self, usuario_id):
        try:
            query = "SELECT id, titulo, contenido FROM textos WHERE usuario_id = %s"
            self.cursor.execute(query, (usuario_id,))
            documentos = self.cursor.fetchall()
            return documentos
        except mysql.connector.Error as err:
            print(f"Error al obtener documentos: {err}")
            return []

    def obtener_documento_por_id(self, usuario_id, documento_id):
        try:
            query = "SELECT id, contenido FROM textos WHERE usuario_id = %s AND id = %s"
            self.cursor.execute(query, (usuario_id, documento_id))
            documento = self.cursor.fetchone()
            return documento
        except mysql.connector.Error as err:
            print(f"Error al obtener documento por ID: {err}")
            return None

    def obtener_id_usuario(self, correo):
        try:
            query = "SELECT id FROM usuarios WHERE correo = %s"
            self.cursor.execute(query, (correo,))
            user_id = self.cursor.fetchone()
            if user_id:
                return user_id[0]
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error al obtener ID del usuario: {err}")
            return None
        
    def borrar_documento(self, documento_id):
        try:
            query = "DELETE FROM textos WHERE id = %s"
            self.cursor.execute(query, (documento_id,))
            self.connection.commit()
            return "Documento borrado correctamente."
        except mysql.connector.Error as err:
            return f"Error al borrar el documento: {err}"
        
    def actualizar_contenido_documento(self, documento_id, nuevo_contenido):
        try:
            query = "UPDATE textos SET contenido = %s WHERE id = %s"
            values = (nuevo_contenido, documento_id)
            self.cursor.execute(query, values)
            self.connection.commit()
            return "Contenido del documento actualizado correctamente."
        except mysql.connector.Error as err:
            return f"Error al actualizar el contenido del documento: {err}"




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

# Parece ser que esta no se usa en ningún momento
def verificar_credenciales_en_bd(correo, contrasena, cursor):
    query = "SELECT id FROM usuarios WHERE correo = ? AND contraseña = ?"
    cursor.execute(query, (correo, contrasena))
    user_id = cursor.fetchone()
    return user_id

def enviar_correo_restablecer(correo):
    token = generar_token(correo)
    url_restablecer = url_for('auth.restablecer_contrasena', token=token, _external=True)

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
