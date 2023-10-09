import tkinter as tk
from tkinter import messagebox, ttk
from bbdd import DatabaseManager

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Interfaz de Usuario")
        self.geometry("400x300")
        self.create_widgets()

        # Configurar el estilo para los botones
        estilo = ttk.Style()
        estilo.configure("TButton", padding=10, font=("Arial", 12), background="green", foreground="white")

    def create_widgets(self):
        tk.Label(self, text="Bienvenido", font=("Arial", 14), bg="blue", fg="white").pack(pady=20)

        # Usar botones con el estilo configurado
        ttk.Button(self, text="Registrarse", command=self.open_registro).pack(pady=20)
        ttk.Button(self, text="Iniciar Sesión", command=self.open_inicio_sesion).pack(pady=20)

    def open_registro(self):
        self.withdraw()  # Ocultar la ventana principal
        registro_window = RegistroVentana(self)
        registro_window.wait_window()  # Esperar hasta que la ventana de registro se cierre
        self.deiconify()  # Mostrar la ventana principal nuevamente

    def open_inicio_sesion(self):
        self.withdraw()  # Ocultar la ventana principal
        inicio_sesion_window = InicioSesionVentana(self)
        inicio_sesion_window.wait_window()  # Esperar hasta que la ventana de inicio de sesión se cierre
        self.deiconify()  # Mostrar la ventana principal nuevamente

class RegistroVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro")
        self.geometry("400x300")
        
        self.db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Correo:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Registrar", command=self.register_user).pack(pady=20)

    def register_user(self):
        correo = self.email_entry.get()
        contrasena = self.password_entry.get()

        if correo and contrasena:   
            if self.db_manager.register_user(correo, contrasena):
                messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
                self.destroy() 
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario.")
        else:
            messagebox.showerror("Error", "Correo y contraseña son obligatorios.")

class InicioSesionVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inicio de Sesión")
        self.geometry("300x200")
        
        self.db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Correo:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Iniciar Sesión", command=self.login_user).pack(pady=20)

    def login_user(self):
        correo = self.email_entry.get()
        contrasena = self.password_entry.get()

        if correo and contrasena:   
            if self.db_manager.login(correo, contrasena):
                messagebox.showinfo("Inicio de Sesión Exitoso", "Sesión iniciada correctamente.")
                self.destroy()  
            else:
                messagebox.showerror("Error", "Inicio de sesión fallido. Verifique su correo y contraseña.")
        else:
            messagebox.showerror("Error", "Correo y contraseña son obligatorios.")

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
