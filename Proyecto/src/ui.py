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
    success = None

    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        confirmar_contrasena = request.form['confirmar_contrasena']

        error , success= db_manager.register_user(correo, contrasena, confirmar_contrasena)

    return render_template('registro.html', error=error, success = success)


@auth_bp.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    error = None

    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if correo and contrasena:
            success, error_message = db_manager.login(correo, contrasena)
            if success:
                return redirect(url_for('auth.restricted'))
            else:
                error = error_message or "Credenciales incorrectas"
        else:
            error = "Correo y contraseña son obligatorios"

    return render_template('inicio_sesion.html', error=error)


@auth_bp.route('/restricted', methods=['GET', 'POST'])
def restricted():
    return render_template('restricted.html')







