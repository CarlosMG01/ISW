# Abrir el archivo en modo lectura
with open('/usr/local/lib/python3.9/site-packages/pygoogletranslation/utils.py', 'r') as file:
    lines_gl = file.readlines()  # Leer todas las líneas del archivo
    lines_gl[7] = "from pygoogletranslation.models import TranslatedPart\n"  # Modificar la línea

with open('/usr/local/lib/python3.9/site-packages/pygoogletranslation/utils.py', 'w') as file:
    file.writelines(lines_gl)  # Escribir las líneas modificadas de vuelta al archivo

with open('/usr/local/lib/python3.9/site-packages/pytesseract/pytesseract.py', 'r') as file:
    lines = file.readlines()  # Leer todas las líneas del archivo
    lines[29] = "tesseract_cmd = '/usr/bin/tesseract'\n"  # Modificar la línea

# Escribir de nuevo al archivo
with open('/usr/local/lib/python3.9/site-packages/pytesseract/pytesseract.py', 'w') as file:
    file.writelines(lines)  # Escribir las líneas modificadas de vuelta al archivo
