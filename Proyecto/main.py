from flask import Flask
from flask_mail import Mail
import webbrowser
from src import auth_bp, home_bp
import os

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)

app.testing = True

def install_dependencies():
    os.system("pip install -r requitements.txt")


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'practicaceu@gmail.com'
app.config['MAIL_PASSWORD'] = 'lkytkgkbhirfyxlv'
mail = Mail(app)

app.secret_key = '12345'

if __name__ == '__main__':
    url = "http://127.0.0.1:5000"
   
    webbrowser.open(url)

    app.run(debug=False)
