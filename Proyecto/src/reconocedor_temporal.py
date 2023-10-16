from flask import Flask, render_template, request
from PIL import Image
import pytesseract
import sys

def extraer_texto():
    texto_extraido =pytesseract.image_to_string(file_name)
    return texto_extraido
