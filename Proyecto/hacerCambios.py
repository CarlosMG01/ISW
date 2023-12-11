# Abrir el archivo en modo lectura
with open('./src/bbdd.py', 'r') as file:
    lines = file.readlines()  # Leer todas las líneas del archivo
    lines[21] = "docker = 1\n"  # Modificar la línea

# Escribir de nuevo al archivo
with open('./src/bbdd.py', 'w') as file:
    file.writelines(lines)  # Escribir las líneas modificadas de vuelta al archivo

# Leer el archivo ui.py
with open('./src/ui.py', 'r') as file:
    lines_ui = file.readlines()  # Leer todas las líneas del archivo ui.py
    lines_ui[23] = "docker = 1\n"

with open('./src/ui.py', 'w') as file:
    file.writelines(lines_ui)  # Escribir las líneas modificadas de vuelta al archivo

