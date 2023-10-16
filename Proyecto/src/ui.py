import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, render_template, request, redirect, url_for, session
from .bbdd import DatabaseManager
import re

auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)


db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')

@home_bp.route('/')
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

        # enlace_verificacion = "http://127.0.0.1/verificar?token=abcd1234" # Tendría que generarse token

        # enviar_correo_verificacion(correo, enlace_verificacion) # Tendría que registrarse al dar al enlace


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

@auth_bp.route('/cambio_contrasena', methods=['GET', 'POST'])
def cambio_contrasena():
    error = None
    success = None

    if request.method == 'POST':
        correo = request.form['correo']
        contrasena_actual = request.form['contrasena_actual']
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_nueva_contrasena = request.form['confirmar_nueva_contrasena']

        if nueva_contrasena != confirmar_nueva_contrasena:
            error = "Las contraseñas nuevas no coinciden"
        else:
            error, success = db_manager.change_password(correo, contrasena_actual, nueva_contrasena)

    return render_template('cambio_contrasena.html', error=error, success=success)


@auth_bp.route('/restricted', methods=['GET', 'POST'])
def restricted():
    return render_template('restricted.html')





'''
def enviar_correo_verificacion(correo, enlace_verificacion):
    
    servidor_smtp = "smtp.gmail.com"  
    puerto = 587
    usuario = "ocr.iswceu@gmail.com"
    contraseña = "Practica_Ingenieria_Software"

    mensaje = MIMEMultipart()
    mensaje['From'] = usuario
    mensaje['To'] = correo
    mensaje['Subject'] = "Verificación de Correo Electrónico"

    cuerpo = f"Para verificar tu correo electrónico, haz clic en el siguiente enlace: {enlace_verificacion}"
    mensaje.attach(MIMEText(cuerpo, 'plain'))

    try:
        with smtplib.SMTP(servidor_smtp, puerto) as server:
            server.starttls()
            server.login(usuario, contraseña)
            server.sendmail(usuario, correo, mensaje.as_string())

            print("Correo enviado con éxito")
    except smtplib.SMTPAuthenticationError as e:
        print("Error de autenticación SMTP: Credenciales incorrectas.")
    except smtplib.SMTPExeption as e:
        print(f"Error SMTP general: {e}")

'''
# Función de ruta posterior. Primero centrarse en que se envía el correo
'''
@auth_bp.route('/verificar', methods=['GET'])
def verificar():
    token = request.args.get('token')

    usuario = db_manager.buscar_usuario_por_token(token) # Crearlo en bbdd.py

    if usuario:
        db_manager.marcar_usuario_como_verificado(usuario['id'])
        return "Correo verificado con éxito"
    else:
        return "Error: Token no válido o expirado"
'''
