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
    
    with pytest.raises(ValueError, match="Correo y contraseña son obligatorios"):
        db_manager.register_user("", "password123")

    with pytest.raises(ValueError, match="Correo y contraseña son obligatorios"):
        db_manager.register_user("test@example.com", "")


def test_duplicate_email_registration():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    db_manager.cursor.execute("DELETE FROM usuarios WHERE correo='test@example.com'")
    db_manager.register_user("test@example.com", "password123")
    with pytest.raises(ValueError):
        db_manager.register_user("test@example.com", "otracontrasena")


def test_login_successful():
    db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
    db_manager.register_user('test@example.com', 'password123')
    assert db_manager.login('test@example.com', 'password123') == True
