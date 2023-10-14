from flask import Flask
from src import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.testing = True

if __name__ == '__main__':
    app.run(debug=True)
