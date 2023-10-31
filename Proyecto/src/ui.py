import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import Flask, render_template, request, jsonify
from .bbdd import DatabaseManager
from .bbdd import confirmar_correo_en_bd, enviar_correo_verificacion, obtener_correo_desde_token,login, enviar_correo_restablecer
import re
import pytesseract
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)


db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
correo_electronico=""
imagen_perfil= "/static/perfil.png"

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
        error, success = db_manager.register_user(correo, contrasena, confirmar_contrasena)  

        if success:            
            enviar_correo_verificacion(correo, contrasena) 
            print(contrasena)
            

            success= 'Se ha enviado un correo de confirmación a tu dirección de correo electrónico.'
            session['correo_usuario'] = correo
            return render_template('inicio_sesion.html', error=error, success=success)

    return render_template('registro.html', error=error, success=success)




@auth_bp.route('/confirmar-correo/<token>')
def confirmar_correo(token):
    correo = obtener_correo_desde_token(token)
    contrasena = request.args.get('contrasena')

    if correo and contrasena :
        cursor = db_manager.cursor
        connection = db_manager.connection

        confirmar_correo_en_bd(correo,contrasena, cursor, connection)
        success = "Su correo se ha validado con éxito"
        return render_template('inicio_sesion.html', correo=correo, success=success)
    else:
        return render_template('inicio_sesion.html', error='Token inválido o expirado')




@auth_bp.route('/inicio_sesion', methods=['GET', 'POST'])
def inicio_sesion():
    error = None

    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        if correo and contrasena:
            success, error_message = login(correo, contrasena, db_manager.cursor)
            if success:
                guardar_valores(correo)
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
        contrasena_actual = request.form['contrasena_actual']
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_nueva_contrasena = request.form['confirmar_nueva_contrasena']

        if nueva_contrasena != confirmar_nueva_contrasena:
            error = "Las contraseñas nuevas no coinciden"
        else:
            correo = session.get('correo_usuario')
            error, success = db_manager.change_password(correo, contrasena_actual, nueva_contrasena)

    return render_template('cambio_contrasena.html', error=error, success=success)


@auth_bp.route('/restricted', methods=['GET', 'POST'])
def restricted():
    resultado =""
    if request.method == 'POST': 
        file = request.files['file']
        if file:
            # Utiliza pytesseract para extraer texto de la imagen
            file.save(os.path.join('static', file.filename))
            texto_extraido = pytesseract.image_to_string(os.path.join('static',file.filename))
            # Imprime el texto extraído
            resultado = texto_extraido

    return render_template('restricted.html', resultado=resultado)

@auth_bp.route('/perfil-usuario', methods =['GET','POST'])
def perfil():
    correo = guardar_valores()
    imagen_perfil = db_manager.obtener_imagen_perfil(correo)
    imagen_predeterminada = "/static/perfil.png"

    if  request.method =='POST':
        nueva_imagen_perfil = request.files['nueva_imagen']
        if nueva_imagen_perfil:
            # Verifica que la extensión del archivo sea válida (puedes personalizar esto)
            if nueva_imagen_perfil.filename != '' and nueva_imagen_perfil.filename.endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp')):
                filename = secure_filename(nueva_imagen_perfil.filename)
                nueva_imagen_path = os.path.join('static', filename)
                if not os.path.exists('static'):
                    os.makedirs('static')

                nueva_imagen_perfil.save(nueva_imagen_path)
                imagen_perfil = nueva_imagen_path
                # Actualiza la imagen de perfil en la base de datos
                result = db_manager.guardar_imagen_perfil(correo, nueva_imagen_path)
                if result:
                    return render_template('perfil-usuario.html', imagen_perfil=imagen_perfil, correo=correo, success=result)
            else:
                error = "Formato de imagen no válido. Por favor, utiliza archivos de imagen (.jpg, .png, .jpeg, .gif, .bmp)."
    if imagen_perfil is None:
        imagen_perfil = imagen_predeterminada

    return render_template('perfil-usuario.html', imagen_perfil=imagen_perfil, correo=correo)

@auth_bp.route('/chat', methods =['GET','POST'])
def chat():
    correo = guardar_valores()
    return render_template('chat.html',correo=correo)

def guardar_valores(correo=None):
    global correo_electronico
    if correo is None:
        return correo_electronico
    else:
        correo_electronico = correo
        return True
    
@auth_bp.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

def ayuda():
    return render_template('ayuda.html')


@auth_bp.route('/olvido_contrasena', methods=['GET', 'POST'])
def olvide_contrasena():
    if request.method == 'POST':
        correo = request.form['correo']

        if correo:
            # Generar el token y enviar el correo.
            enviar_correo_restablecer(correo)

            flash('Se ha enviado un enlace de restablecimiento de contraseña a tu dirección de correo electrónico.', 'success')
            return redirect(url_for('auth.inicio_sesion'))
        else:
            flash('Por favor, proporciona una dirección de correo electrónico válida.', 'error')

    return render_template('olvido_contrasena.html') 