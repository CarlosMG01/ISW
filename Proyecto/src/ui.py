import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from flask import Flask, render_template, request, jsonify, send_file, abort
from .bbdd import DatabaseManager
from .bbdd import confirmar_correo_en_bd, enviar_correo_verificacion, obtener_correo_desde_token,login, enviar_correo_restablecer
#guardar_documento, obtener_textos
from fpdf import FPDF
import fitz # pip install pymupdf
from docx import Document
from googletrans import Translator
from datetime import datetime
import googletrans
import re
import pytesseract
import os
from werkzeug.utils import secure_filename
from io import BytesIO
from uuid import uuid4



docker = 0

auth_bp = Blueprint('auth', __name__)
home_bp = Blueprint('home', __name__)

if docker == 1:
    db_manager = DatabaseManager('mysql-container', 'root', 'root', 'prueba')
else:
    db_manager = DatabaseManager('localhost', 'carlos', 'root', 'prueba')

messages = []   
resultado_global = ""
translator = Translator()
resultado_global_traducido = ""
contador_archivos = 0

def obtener_id_usuario_actual():
    correo = session.get('correo_usuario')
    if correo:
        return db_manager.obtener_id_usuario(correo)
    else:
        return None


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
            file.save(os.path.join('static', file.filename))
            _, file_extension = os.path.splitext(file.filename)

            if file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
                # Utilizar pytesseract para extraer texto de la imagen
                texto_extraido = pytesseract.image_to_string(os.path.join('static', file.filename))
            elif file_extension.lower() == '.pdf':
                # Utilizar fpdf para extraer texto de un archivo PDF
                texto_extraido = extract_text_from_pdf(os.path.join('static', file.filename))
            elif file_extension.lower() == '.docx':
                # Utilizar python-docx para extraer texto de un archivo Word
                texto_extraido = extract_text_from_docx(os.path.join('static', file.filename))
            else:
                # Manejar otros tipos de archivos o mostrar un mensaje de error
                texto_extraido = "Tipo de archivo no admitido."

            # Imprime el texto extraído
            resultado_global = texto_extraido
            usuario_id = obtener_id_usuario_actual()
            if usuario_id is not None:
                titulo = "Documento"
                db_manager.guardar_documento(usuario_id, titulo, texto_extraido)

    return render_template('restricted.html', resultado=resultado_global)
#PDF
def extract_text_from_pdf(pdf_path):
    text = ''
    with fitz.open(pdf_path) as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text()

    return text
#WORD
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

# PDF
@auth_bp.route('/convertir-a-pdf', methods=['POST'])
def convertir_a_pdf():
    global resultado_global

    pdf_output = BytesIO()

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(190, 10, txt='PDF extraído de OCRTeam', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(190, 10, txt=resultado_global, border=0, align='L')

    pdf_output.write(pdf.output(dest='S').encode('latin1'))

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'mitexto_{timestamp}.pdf'

    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name=filename)


# WORD
@auth_bp.route('/convertir-a-word', methods=['POST'])
def convertir_a_word():
    global resultado_global

    docx_output = BytesIO()

    document = Document()
    document.add_heading('Documento Word extraído de OCRTeam', 0)
    document.add_paragraph(resultado_global)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'mitexto_{timestamp}.docx'

    document.save(docx_output)

    docx_output.seek(0)

    return send_file(docx_output, as_attachment=True, download_name=filename)


# Traductor - Inglés
@auth_bp.route('/translate-en', methods=['GET'])
def translate_text():
    global resultado_global
    if resultado_global:
        translated = translator.translate(resultado_global, src="es", dest="en")
        return jsonify({"translated_text": translated.text})
    else:
        return jsonify({"error": "No hay texto para traducir"})

# Nuevas rutas para traducir a otros idiomas
@auth_bp.route('/translate-fr', methods=['GET'])
def translate_to_french():
    global resultado_global
    if resultado_global:
        translated = translator.translate(resultado_global, src="es", dest="fr")
        return jsonify({"translated_text": translated.text})
    else:
        return jsonify({"error": "No hay texto para traducir"})

@auth_bp.route('/translate-it', methods=['GET'])
def translate_to_italian():
    global resultado_global
    if resultado_global:
        translated = translator.translate(resultado_global, src="es", dest="it")
        return jsonify({"translated_text": translated.text})
    else:
        return jsonify({"error": "No hay texto para traducir"})

@auth_bp.route('/translate-pt', methods=['GET'])
def translate_to_portuguese():
    global resultado_global
    if resultado_global:
        translated = translator.translate(resultado_global, src="es", dest="pt")
        return jsonify({"translated_text": translated.text})
    else:
        return jsonify({"error": "No hay texto para traducir"})

#Perfil
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


@auth_bp.route('/mistextos', methods=['GET'])
def mistextos():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
    else:
        correo = session.get('correo_usuario')
        usuario_id = obtener_id_usuario_actual()
        if usuario_id is not None:
            documentos = db_manager.obtener_documentos(usuario_id)
            return render_template('mistextos.html', correo=correo, documentos=documentos)
        else:
            return "Error al obtener ID del usuario."

@auth_bp.route('/generar-pdf/<int:id>', methods=['GET'])
def generar_pdf(id):
    usuario_id = obtener_id_usuario_actual()

    if usuario_id is not None:
        documento = db_manager.obtener_documento_por_id(usuario_id, id)

        if documento is not None:

            contenido = documento[1]
            
            pdf_output = BytesIO()
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(190, 10, txt='PDF extraído de OCRTeam', ln=True, align='C')
            pdf.set_font('Arial', '', 12)
            pdf.multi_cell(190, 10, txt=contenido, border=0, align='L')
            pdf_output.write(pdf.output(dest='S').encode('latin1'))


            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f'mitexto_{timestamp}.pdf'

            pdf_output.seek(0)
            
            return send_file(pdf_output, download_name=filename, as_attachment=True)
        else:
            return "Documento no encontrado."
    else:
        return "Error al obtener ID del usuario."

@auth_bp.route('/generar-word/<int:id>', methods=['GET'])
def generar_word(id):
    usuario_id = obtener_id_usuario_actual()

    if usuario_id is not None:
        documento = db_manager.obtener_documento_por_id(usuario_id, id)

        if documento is not None:
            contenido = documento[1]

            docx_output = BytesIO()
            document = Document()
            document.add_heading('Documento Word extraído de OCRTeam', 0)   
            document.add_paragraph(contenido)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f'mitexto{timestamp}.docx'

            document.save(docx_output)
            docx_output.seek(0)
            
            # Devolver el Word como respuesta para descargar
            return send_file(docx_output, download_name=filename, as_attachment=True)
        else:
            return "Documento no encontrado."
    else:
        return "Error al obtener ID del usuario."
    
@auth_bp.route('/borrar-texto/<int:id>', methods=['GET'])
def borrar_texto(id):
    usuario_id = obtener_id_usuario_actual()

    if usuario_id is not None:

        documento = db_manager.obtener_documento_por_id(usuario_id, id)

        if documento is not None:
            db_manager.borrar_documento(id)
            flash('Texto borrado correctamente', 'success')
        else:
            flash('No se puede borrar el texto. El documento no pertenece al usuario actual.', 'error')
    else:
        flash('Error al obtener ID del usuario.', 'error')

    return redirect(url_for('auth.mistextos'))

@auth_bp.route('/editar-texto/<int:id>', methods=['GET', 'POST'])
def editar_texto(id):
    usuario_id = obtener_id_usuario_actual()

    if usuario_id is not None:
        documento = db_manager.obtener_documento_por_id(usuario_id, id)

        if documento is not None:
            if request.method == 'POST':
                nuevo_contenido = request.form['nuevo_contenido']
                db_manager.actualizar_contenido_documento(id, nuevo_contenido)
                flash('Texto actualizado correctamente', 'success')
                return redirect(url_for('auth.mistextos'))

            return render_template('editar_texto.html', documento=documento)
        else:
            return "Documento no encontrado."
    else:
        return "Error al obtener ID del usuario."

 



@auth_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
    user = str(uuid4())
    avatar = f'https://robohash.org/{user}?bgset=bg2'
    
    if 'user' not in session:
        session['user'] = str(uuid4())
        session['avatar'] = f'https://robohash.org/{session["user"]}?bgset=bg2'

    user = session['user']
    avatar = session['avatar']

    if request.method == 'POST':
        text = request.form.get('text', '')
        messages.append((user, avatar, text))

    correo = session.get('correo_usuario')
    return render_template('chat.html', user=user, avatar=avatar, messages=messages, correo=correo)

#def chat_messages(own_id, messages):
#    processed_messages = []
#    for user_id, avatar, text in messages:
#        sent_by_own_id = user_id == own_id
#        processed_messages.append({
#            'avatar': avatar,
#            'text': text,
#            'sent_by_own_id': sent_by_own_id
#        })
#    return processed_messages




@auth_bp.route('/ayuda')
def ayuda():
    if not session.get('logged_in'):
        return redirect(url_for('auth.inicio_sesion'))
    return render_template('ayuda.html')


@auth_bp.route('/olvido_contrasena', methods=['GET', 'POST'])
def olvide_contrasena(): 
    error = None

    if request.method == 'POST':
        correo = request.form['correo']
        if correo:
            error, success = db_manager.verificar_usuario_por_correo(correo)
            if success:
                enviar_correo_restablecer(correo)
                return render_template('inicio_sesion.html', error=error, success=success)
        else:
            return render_template('olvido_contrasena.html', error = error)

    return render_template('olvido_contrasena.html', error = error)

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
