import tkinter as tk
from tkinter import messagebox
from bbdd import DatabaseManager

class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Interfaz de Usuario")
        self.geometry("700x400")
        
        self.db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Correo:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Registrar", command=self.register_user).pack()

    def register_user(self):
        correo = self.email_entry.get()
        contrasena = self.password_entry.get()

        if correo and contrasena:
            if self.db_manager.register_user(correo, contrasena):
                messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario.")
        else:
            messagebox.showerror("Error", "Correo y contraseña son obligatorios.")

if __name__ == "__main__":
    app = GUI()
    app.mainloop()
