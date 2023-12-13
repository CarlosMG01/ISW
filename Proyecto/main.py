from flask import Flask
from flask_mail import Mail
import webbrowser
from src import auth_bp, home_bp,chat_bp
import os, sys, ipaddress

from chatapp import create_app, socketio  # Importa create_app y socketio desde el módulo chatapp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(chat_bp)

app.testing = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'
mail = Mail(app)

app.secret_key = '12345'

ip, port = '', 5000

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ip_port = sys.argv[1]
        if ":" in ip_port:
            ip, port = ip_port.split(":")
        else:
            ip, port = [ip_port, "5000"]
        try:
            f = ipaddress.IPv4Address(ip)
            url = f"http://{ip}:{port}"
            port = int(port)
        except:
            url = "http://127.0.0.1:5000"
            ip, port = "127.0.0.1", 5000
    else:
        url = "http://127.0.0.1:5000"
        ip, port = "127.0.0.1", 5000

    webbrowser.open(url)

    # Crea la aplicación Flask y el objeto Socket.IO
    socketio.init_app(app)
    

    # Ejecuta la aplicación Flask con Socket.IO
    socketio.run(app, debug=False, host="0.0.0.0")
