import tkinter as tk
import sqlite3
from tkinter import messagebox

# Variables globales para los campos de entrada del registro y la ventana de inicio de sesion
correo_entry = None
usuario_entry = None
password_entry = None
confirm_password_entry = None
ventana_inicio_sesion = None

# Variable global para almacenar el nombre de usuario despues del inicio de sesion
usuario_actual = None

# Funcion para registrar un nuevo usuario
def registrar_usuario():
    global correo_entry, usuario_entry, password_entry, confirm_password_entry
    
    # Obtener los datos del formulario de registro
    correo = correo_entry.get()
    nombre_usuario = usuario_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Verificar si todos los campos estan llenos
    if correo and nombre_usuario and password == confirm_password:
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
            confirm_password_entry.delete(0, tk.END)
            
            # Mostrar un mensaje de exito
            messagebox.showinfo("Registro Exitoso", "Usuario registrado con exito.")
            # Cierro mi pestana de registro
       
        #Mostrar mensajes de error
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")
    else:
        messagebox.showerror("Campos Incompletos o no coindicden las contrasenas", "Por favor, complete todos los campos.")

# Funcion para iniciar sesion
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
               # Almacenar el nombre de usuario actual
               usuario_actual = usuario
               #Ocultar la ventana de inicio de sesion
               ventana_principal.destroy()
               # Mostrar la ventana del "home" de la
               mostrar_ventana_home()         
            
        else:
            messagebox.showerror("Error", "Usuario o password incorrectos.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al iniciar sesion: {str(e)}")

# Funcion para mostrar la ventana "home" 
def mostrar_ventana_home():
    ventana_home = tk.Toplevel(ventana_principal1)
    ventana_home.title(f"Bienvenido, {usuario_actual}")
    ventana_principal1.withdraw()
    cambiarpass_button = tk.Button(ventana_home, text="Cambiar contrasena", command=cambiar_passw)
    cambiarpass_button.pack()

    # Este home es el de nuestra aplicacion. 
    # Habria que hacer que si inicio de sesion exitoso te lleve al home linea 78-85
# Funcion para abrir la ventana de registro
def abrir_ventana_registro():
    global correo_entry, usuario_entry, password_entry, confirm_password_entry, ventana_inicio_sesion
    
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
    
    tk.Label(ventana_registro, text="confirm password").pack()
    confirm_password_entry = tk.Entry(ventana_registro, show="*")
    confirm_password_entry.pack()

    registrar_button = tk.Button(ventana_registro, text="Registrar", command=registrar_usuario)
    registrar_button.pack()

def cambiar_passw():
    global usuario_actual
    
    # Crear una nueva ventana para cambiar la contrasena
    ventana_cambio_passw = tk.Toplevel(ventana_principal1)
    ventana_cambio_passw.title("Cambiar Contrasena")

    # Crear etiquetas y campos de entrada para el cambio de contrasena
    tk.Label(ventana_cambio_passw, text=f"Cambiar contrasena para {usuario_actual}").pack()

    tk.Label(ventana_cambio_passw, text="Contrasena Actual:").pack()
    contrasena_actual_entry = tk.Entry(ventana_cambio_passw, show="*")
    contrasena_actual_entry.pack()

    tk.Label(ventana_cambio_passw, text="Nueva Contrasena:").pack()
    nueva_contrasena_entry = tk.Entry(ventana_cambio_passw, show="*")
    nueva_contrasena_entry.pack()
    
    tk.Label(ventana_cambio_passw, text="Confirmar Nueva Contrasena:").pack()
    confirmar_nueva_contrasena_entry = tk.Entry(ventana_cambio_passw, show="*")
    confirmar_nueva_contrasena_entry.pack()

    # Agregar un boton para cambiar la contrasena
    cambiar_contrasena_button = tk.Button(ventana_cambio_passw, text="Cambiar Contrasena", command=lambda: cambiar_contrasena_confirmado(contrasena_actual_entry.get(), nueva_contrasena_entry.get(), confirmar_nueva_contrasena_entry.get()))
    cambiar_contrasena_button.pack()

# Funcion para cambiar la contrasena en la base de datos
def cambiar_contrasena_confirmado(contrasena_actual, nueva_contrasena, confirmar_nueva_contrasena):
    global usuario_actual
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        # Verificar si la contrasena actual coincide con la almacenada en la base de datos
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = ? AND password = ?", (usuario_actual, contrasena_actual))
        usuario_encontrado = cursor.fetchone()

        if usuario_encontrado:
            # Verificar si las dos nuevas contrasenas coinciden
            if nueva_contrasena == confirmar_nueva_contrasena:
                # Actualizar la contrasena en la base de datos
                cursor.execute("UPDATE usuarios SET password = ? WHERE nombre_usuario = ?", (nueva_contrasena, usuario_actual))
                conn.commit()
                conn.close()

                # Mostrar un mensaje de exito
                messagebox.showinfo("Contrasena Cambiada", "La contrasena se ha cambiado con exito.")
            else:
                messagebox.showerror("Error", "Las nuevas contrasenas no coinciden.")
        else:
            messagebox.showerror("Error", "Contrasena actual incorrecta. No se pudo cambiar la contrasena.")

    except Exception as e:
        messagebox.showerror("Error", f"Error al cambiar la contrasena: {str(e)}")

    
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

# Boton para abrir la ventana de registro
registrar_usuario_button = tk.Button(ventana_principal, text="Registrar Usuario", command=abrir_ventana_registro)
registrar_usuario_button.pack()

ventana_principal1 = tk.Tk()
ventana_principal1.title("Inicio de sesion")

ventana_principal1.withdraw()
ventana_principal.mainloop()
