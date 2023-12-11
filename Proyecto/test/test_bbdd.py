import sys
import pytest
import mysql.connector
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.bbdd import DatabaseManager
from src.bbdd import login


def test_register_user():
    db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
    db_manager.cursor.execute("DELETE FROM usuarios WHERE correo='test@example.com'")
    
    # Realiza el registro y verifica el resultado
    error, success = db_manager.register_user('test@example.com', 'Password123', 'Password123')
    assert success == 'formulario completado'
    assert error is None

def test_register_user_missing_fields():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")

    response =db_manager.register_user("", "Password123","Password123")
    assert response == ('Correo y contraseña son obligatorios', None)

    
    response2 =db_manager.register_user("test@example.com", "","Password123") 
    assert response2 == ('Correo y contraseña son obligatorios', None)

    response3 =db_manager.register_user("test@example.com", "Password123","") 
    assert response3 == ('Correo y contraseña son obligatorios', None)


def test_duplicate_email_registration():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    db_manager.insert_user_directly('pruebapracticasw@gmail.com', 'Password123') # registro manual 
    # Intenta registrar un usuario con un correo duplicado
    error,_=db_manager.register_user('pruebapracticasw@gmail.com', 'Password1234', 'Password1234')
    assert error == 'Este correo electrónico ya está en uso. Por favor, elige otro.'
    

def test_login_successful():
    db_manager = DatabaseManager('localhost', 'root', 'root', 'prueba')
    
    cursor = db_manager.cursor
    assert login('pruebapracticasw@gmail.com', 'Prueba12345', cursor)

def test_login_missing_fields():
    
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    db_manager.delete_user_manually('pruebapracticasw@gmail.com') # borrado manual 
    cursor = db_manager.cursor 
    _,error = login('pruebapracticasw@gmail.com', '', cursor)
    assert  error == "Correo y contraseña son obligatorios"
    
   

def test_login_with_incorrect_email():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    cursor = db_manager.cursor 
    _,error = login("nonexistent@example.com", "Password123", cursor)
    assert  error == "Credenciales incorrectas"

def test_login_with_incorrect_password():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    cursor = db_manager.cursor 
    assert login("test@example.com", "wrong_password", cursor) == False


def test_register_user_wrong_email():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    response = db_manager.register_user("hola", "Password123", "Password123")
    assert response == ("Formato de correo incorrecto",None)

def test_register_user_wrong_email2():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    response = db_manager.register_user("hola@gmail", "Password123", "Password123")
    assert response == ("Formato de correo incorrecto",None)


def test_register_different_password_and_confirm_password():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    response = db_manager.register_user("hola@gmail.com", "Password123", "Password1234")
    assert response == ("Las Contraseñas no coinciden",None)

def test_register_invalid_password():
    db_manager = DatabaseManager("localhost", "root", "root", "prueba")
    response = db_manager.register_user("hola@gmail.com", "pass", "pass")
    assert response == ("La contraseña debe tener al menos 5 caracteres, una mayúscula, una minúscula y un número.",None)