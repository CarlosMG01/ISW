import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask import Flask, render_template, request, jsonify, send_file
from .bbdd import DatabaseManager
from .bbdd import confirmar_correo_en_bd, enviar_correo_verificacion, obtener_correo_desde_token,login, enviar_correo_restablecer
from fpdf import FPDF
from docx import Document
import re
import pytesseract
import pdfkit
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)


db_manager = DatabaseManager('localhost', 'carlos', 'root', 'prueba')

resultado_global = ""

@home_bp.route('/')
def index():
    session.clear()
    return redirect(url_for('auth.restricted'))

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.restricted'))

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
                session['correo_usuario'] = correo
                session['logged_in'] = True
                return redirect(url_for('auth.restricted'))
            else:
                error = error_message or "Credenciales incorrectas"
        else:
            error = "Correo y contraseña son obligatorios"

    return render_template('inicio_sesion.html', error=error)

@auth_bp.route('/cambio_contrasena', methods=['GET', 'POST'])
def cambio_contrasena():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
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
    global resultado_global
    if request.method == 'POST': 
        file = request.files['file']
        if file:
            # Utiliza pytesseract para extraer texto de la imagen
            file.save(os.path.join('static', file.filename))
            # static es donde se guardan las iamgenes
            texto_extraido = pytesseract.image_to_string(os.path.join('static',file.filename))
            # Imprime el texto extraído
            resultado_global = texto_extraido

    return render_template('restricted.html', resultado=resultado_global)

# PDF
@auth_bp.route('/convertir-a-pdf', methods=['POST'])
def convertir_a_pdf():
    global resultado_global
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)  
    pdf.cell(190, 10, txt='PDF extraído de OCRTeam', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(190, 10, txt=resultado_global, border=0, align='L')
    pdf_path = 'mitexto.pdf'
    pdf.output(pdf_path)
    
    return send_file(pdf_path, as_attachment=True)

# WORD
@auth_bp.route('/convertir-a-word', methods=['POST'])
def convertir_a_word():
    global resultado_global
    document = Document()
    document.add_heading('Documento word extraído de OCRTeam', 0)

    # Agrega el texto al documento de Word
    document.add_paragraph(resultado_global)

    # Guarda el documento en un archivo .docx
    docx_path = 'mitexto.docx'
    document.save(docx_path)
    
    return send_file(docx_path, as_attachment=True)













@auth_bp.route('/perfil-usuario', methods =['GET','POST'])
def perfil():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
    else:
        correo = session.get('correo_usuario')
        imagen_perfil = db_manager.obtener_imagen_perfil(correo)
        if  request.method =='POST':
            nueva_imagen_perfil = request.files['nueva_imagen']
            if nueva_imagen_perfil:
                # Verifica que la extensión del archivo sea válida (puedes personalizar esto)
                if nueva_imagen_perfil.filename != '' and nueva_imagen_perfil.filename.endswith(('.jpg', '.png', '.jpeg', '.gif', '.bmp')):
                    # Actualiza la imagen de perfil en la base de datos
                    result = db_manager.guardar_imagen_perfil(correo, nueva_imagen_perfil)
                    imagen_perfil = db_manager.obtener_imagen_perfil(correo)
                    if result:
                        return render_template('perfil-usuario.html', imagen_perfil=imagen_perfil, correo=correo, success=result)
                else:
                    error = "Formato de imagen no válido. Por favor, utiliza archivos de imagen (.jpg, .png, .jpeg, .gif, .bmp)."
        return render_template('perfil-usuario.html', imagen_perfil=imagen_perfil, correo=correo)


@auth_bp.route('/mistextos', methods =['GET','POST'])
def mistextos():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
    else:
        correo = session.get('correo_usuario')
        return render_template('mistextos.html', correo=correo)
    
@auth_bp.route('/chat', methods =['GET','POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
    correo = session.get('correo_usuario')
    return render_template('chat.html',correo=correo)

@auth_bp.route('/ayuda')
def ayuda():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
    return render_template('ayuda.html')


@auth_bp.route('/olvido_contrasena', methods=['GET', 'POST'])
def olvide_contrasena(): 
    if request.method == 'POST':
        correo = request.form['correo']

        if correo:
            user_id = db_manager.verificar_usuario_por_correo(correo)
            if user_id:
                # Generar el token y enviar el correo.
                enviar_correo_restablecer(correo)

                flash('Se ha enviado un enlace de restablecimiento de contraseña a tu dirección de correo electrónico.', 'success')
                return redirect(url_for('auth.inicio_sesion'))
        else:
            flash('Por favor, proporciona una dirección de correo electrónico válida.', 'error')

    return render_template('olvido_contrasena.html')

@auth_bp.route('/restablecer_contrasena/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    error = None
    success = None
    nueva_contrasena = None
    confirmar_contrasena = None

    correo = obtener_correo_desde_token(token)
    if request.method == 'POST':
        nueva_contrasena = request.form['nueva_contrasena']
        confirmar_contrasena = request.form['confirmar_nueva_contrasena']

        if nueva_contrasena != confirmar_contrasena:
           error = "Las contraseñas nuevas no coinciden"
        else:
            error, success = db_manager.restablecer_contrasena(correo, nueva_contrasena)

    return render_template('restablecer_contrasena.html', error=error, success=success, token=token)
