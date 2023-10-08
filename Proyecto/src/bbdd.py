import mysql.connector


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
            self.insertar_ejemplo()  # Llamar a la función para insertar ejemplos
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

    def insertar_ejemplo(self):
        try:
            cursor = self.conexion.cursor()
            # Insertar una fila de ejemplo en la tabla de usuarios
            cursor.execute("""
                INSERT INTO usuarios (correo, contraseña)
                VALUES (%s, %s)
            """, ("ejemplo@correo.com", "contraseña123"))

            # Insertar una fila de ejemplo en la tabla de textos
            cursor.execute("""
                INSERT INTO textos (usuario_id, titulo, contenido)
                VALUES (%s, %s, %s)
            """, (1, "Título de ejemplo", "Contenido de ejemplo"))

            self.conexion.commit()
            print("Filas de ejemplo insertadas correctamente.")
        except mysql.connector.Error as err:
            print(f"Error al insertar filas de ejemplo: {err}")


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

    def register_user(self, correo, contrasena):
     if not correo or not contrasena:
            raise ValueError("Correo y contraseña son obligatorios")
     
     try:
            query = "SELECT id FROM usuarios WHERE correo = %s"
            self.cursor.execute(query, (correo,))
            existing_user = self.cursor.fetchone()

            if existing_user:
                raise ValueError("Correo ya registrado, por favor use otro correo.")


            query = "INSERT INTO usuarios (correo, contraseña) VALUES (%s, %s)"
            values = (correo, contrasena)
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
     except mysql.connector.Error as err:
            print(f"Error al registrar usuario: {err}")
            return False

db = BaseDeDatosMariaDB()
db.conectar()
db.desconectar()
