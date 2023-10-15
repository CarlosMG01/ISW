from flask import Flask
import webbrowser
from src import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.testing = True

if __name__ == '__main__':
    url = "http://127.0.0.1:5000"

    webbrowser.open(url)

    app.run(debug=True)
