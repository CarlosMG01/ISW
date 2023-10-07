import sys
import pytest
import mysql.connector
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bbdd import DatabaseManager


def test_register_user():
    db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
    assert db_manager.register_user('test@example.com', 'password123') == True


def test_register_user_missing_fields():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    
    with pytest.raises(ValueError, match="Correo y contraseña son obligatorios"):
        db_manager.register_user("", "password123")

    with pytest.raises(ValueError, match="Correo y contraseña son obligatorios"):
        db_manager.register_user("test@example.com", "")


