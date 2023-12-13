#!/bin/bash

 Actualizar según el sistema operativo
if command -v apt &> /dev/null; then
	apt update
	apt-get install -y tesseract-ocr
elif command -v yum &> /dev/null; then
    yum update
    yum install -y tesseract
else
    echo "Sistema operativo no compatible."
    exit 1
fi

# Ejecutar el script para cambiar la ruta de Tesseract
python3 cambiarRutaTesseract.py

# Ejecutar main.py con parámetros (puedes agregar más parámetros si es necesario)
python3 main.py "$@"
