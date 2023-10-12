from flask import Blueprint, render_template, request, redirect, url_for
from .bbdd import DatabaseManager
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')

@auth_bp.route('/home')
def index():
    return render_template('home.html')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if correo and contrasena:
            if db_manager.register_user(correo, contrasena):
                return "Registro exitoso"
            else:
                return "Error en el registro"
        else:
            return "Correo y contraseña son obligatorios"
    
    return render_template('registro.html')

@auth_bp.route('/inicio-sesion', methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if correo and contrasena:
            if db_manager.login(correo, contrasena):
                return "Inicio de sesión exitoso"
            else:
                return "Credenciales incorrectas"
        else:
            return "Correo y contraseña son obligatorios"
    
    return render_template('inicio_sesion.html')
