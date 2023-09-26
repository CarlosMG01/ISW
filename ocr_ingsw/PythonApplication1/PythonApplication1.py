import tkinter as tk
import sqlite3
from tkinter import messagebox

# Variables globales para los campos de entrada del registro y la ventana de inicio de sesion
correo_entry = None
usuario_entry = None
password_entry = None
ventana_inicio_sesion = None

# Variable global para almacenar el nombre de usuario después del inicio de sesion
usuario_actual = None

# Función para registrar un nuevo usuario
def registrar_usuario():
    global correo_entry, usuario_entry, password_entry
    
    # Obtener los datos del formulario de registro
    correo = correo_entry.get()
    nombre_usuario = usuario_entry.get()
    password = password_entry.get()

    # Verificar si todos los campos están llenos
    if correo and nombre_usuario and password:
        try:
            # Conectar a la base de datos (o crearla si no existe)
            conn = sqlite3.connect("usuarios.db")
            cursor = conn.cursor()

            # Crear la tabla si no existe
            cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               correo TEXT,
                               nombre_usuario TEXT,
                               password TEXT)''')

            # Insertar el nuevo usuario en la base de datos
            cursor.execute("INSERT INTO usuarios (correo, nombre_usuario, password) VALUES (?, ?, ?)",
                           (correo, nombre_usuario, password))
            
            conn.commit()
            conn.close()

            # Limpiar los campos del formulario de registro
            correo_entry.delete(0, tk.END)
            usuario_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

            # Mostrar un mensaje de exito
            messagebox.showinfo("Registro Exitoso", "Usuario registrado con exito.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")
    else:
        messagebox.showerror("Campos Incompletos", "Por favor, complete todos los campos.")

# Función para iniciar sesion
def iniciar_sesion():
    global usuario_actual

    # Obtener los datos del formulario de inicio de sesion
    usuario = usuario_login_entry.get()
    password = password_login_entry.get()

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        # Buscar el usuario en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = ? AND password = ?", (usuario, password))
        usuario_encontrado = cursor.fetchone()
        
        conn.close()

        if usuario_encontrado:
               messagebox.showinfo("Exito", "Inicio de sesion exitoso.")
         #   # Almacenar el nombre de usuario actual
         #   usuario_actual = usuario

            # Ocultar la ventana de inicio de sesion
         #   ventana_inicio_sesion.destroy()

            # Mostrar la ventana del "home" de la
          #  mostrar_ventana_home()
        else:
            messagebox.showerror("Error", "Usuario o password incorrectos.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar sesion: {str(e)}")

# Función para mostrar la ventana "home" de la 
def mostrar_ventana_home():
    ventana_home = tk.Toplevel(ventana_principal)
    ventana_home.title(f"Bienvenido, {usuario_actual}")

    # Aquí puedes diseñar la interfaz de tu ventana "home"

# Función para abrir la ventana de registro
def abrir_ventana_registro():
    global correo_entry, usuario_entry, password_entry, ventana_inicio_sesion
    
    ventana_registro = tk.Toplevel(ventana_principal)
    ventana_registro.title("Registro de Usuario")

    # Crear etiquetas y campos de entrada para el registro de usuario
    tk.Label(ventana_registro, text="Correo:").pack()
    correo_entry = tk.Entry(ventana_registro)
    correo_entry.pack()

    tk.Label(ventana_registro, text="Nombre de Usuario:").pack()
    usuario_entry = tk.Entry(ventana_registro)
    usuario_entry.pack()

    tk.Label(ventana_registro, text="password:").pack()
    password_entry = tk.Entry(ventana_registro, show="*")
    password_entry.pack()

    registrar_button = tk.Button(ventana_registro, text="Registrar", command=registrar_usuario)
    registrar_button.pack()

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Inicio de sesion")

# Crear etiquetas y campos de entrada para el inicio de sesion
tk.Label(ventana_principal, text="Inicio de sesion").pack()
tk.Label(ventana_principal, text="Nombre de Usuario:").pack()
usuario_login_entry = tk.Entry(ventana_principal)
usuario_login_entry.pack()

tk.Label(ventana_principal, text="password:").pack()
password_login_entry = tk.Entry(ventana_principal, show="*")
password_login_entry.pack()

iniciar_sesion_button = tk.Button(ventana_principal, text="Iniciar sesion", command=iniciar_sesion)
iniciar_sesion_button.pack()

# Botón para abrir la ventana de registro
registrar_usuario_button = tk.Button(ventana_principal, text="Registrar Usuario", command=abrir_ventana_registro)
registrar_usuario_button.pack()

ventana_principal.mainloop()