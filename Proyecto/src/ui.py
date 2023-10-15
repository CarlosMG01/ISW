from flask import Blueprint, render_template, request, redirect, url_for, session
from .bbdd import DatabaseManager
from flask import Blueprint
import re

auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)


db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')

@home_bp.route('/home')
def index():
    return render_template('home.html')

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    error = None

    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        # Registrar el usuario en la base de datos
        error= db_manager.register_user(correo, contrasena)

    return render_template('registro.html', error=error)


@auth_bp.route('/inicio_sesion', methods=['GET', 'POST'])
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


