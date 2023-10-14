import pytest
import sys
import os
from flask import Flask, url_for
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.ui import auth_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(auth_bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_registro_form(client):
    response = client.get('/registro')
    assert response.status_code == 200

def test_inicio_sesion_form(client):
    response = client.get('/inicio_sesion')
    assert response.status_code == 200

def test_registro_post_success(client):
    data = {
        'correo': 'test@example.com',
        'contrasena': 'password'
    }
    response = client.post('/registro', data=data)
    assert response.status_code == 200
    assert b"Registro exitoso" in response.data

def test_registro_post_failure(client):
    data = {
        'correo': '',  # Deja el campo de correo en blanco
        'contrasena': 'password'
    }
    response = client.post('/registro', data=data)
    assert response.status_code == 200
    assert b"Correo y contrasena son obligatorios" in response.data

def test_inicio_sesion_post_success(client):
    data = {
        'correo': 'test@example.com',
        'contrasena': 'password'
    }
    response = client.post('/inicio_sesion', data=data)
    assert response.status_code == 200
    assert b"Inicio de sesion exitoso" in response.data

def test_inicio_sesion_post_failure(client):
    data = {
        'correo': 'test@example.com',
        'contrasena': 'incorrect_password'
    }
    response = client.post('/inicio_sesion', data=data)
    assert response.status_code == 200
    assert b"Credenciales incorrectas" in response.data

def test_inicio_sesion_post_blank_fields(client):
    data = {
        'correo': '',  # Deja el campo de correo en blanco
        'contrasena': ''  # Deja el campo de contraseña en blanco
    }
    response = client.post('/inicio_sesion', data=data)
    assert response.status_code == 200
    assert b"Correo y contrasena son obligatorios" in response.data

if __name__ == '__main__':
    pytest.main()