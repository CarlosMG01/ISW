import sys
import pytest
import mysql.connector
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bbdd import DatabaseManager


def test_register_user():
    db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
    assert db_manager.register_user('test@example.com', 'password123') == True


def test_register_user_exception():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    with pytest.raises(mysql.connector.Error):
        db_manager.register_user("test@example.com", "")



