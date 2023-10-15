import sys
import pytest
import mysql.connector
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bbdd import DatabaseManager


def test_register_user():
    db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
    db_manager.cursor.execute("DELETE FROM usuarios WHERE correo='test@example.com'")

    assert db_manager.register_user('test@example.com', 'password123') == True


def test_register_user_missing_fields():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")

    response =db_manager.register_user("", "password123")
    assert response == "Correo y contraseña son obligatorios"

    
    response2 =db_manager.register_user("test@example.com", "")
    assert response2 == "Correo y contraseña son obligatorios"


def test_duplicate_email_registration():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    
    response = db_manager.register_user("test@example.com", "otracontrasena")
    assert response == "Correo ya registrado, por favor use otro correo."



def test_login_successful():
    db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
    assert db_manager.login('test@example.com', 'password123')
    

def test_login_missing_fields():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")  
    with pytest.raises(ValueError, match="Correo y contraseña son obligatorios"):
        db_manager.login("", "password123")
    
    with pytest.raises(ValueError, match="Correo y contraseña son obligatorios"):
        db_manager.login("test@example.com", "")

def test_login_with_incorrect_email():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    assert db_manager.login("nonexistent@example.com", "password123") == False

def test_login_with_incorrect_password():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    
    assert db_manager.login("test@example.com", "wrong_password") == False


def test_register_user_wrong_email():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")

    response = db_manager.register_user("hola", "password123")
    assert response == "Formato de correo incorrecto"



