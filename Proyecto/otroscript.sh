#!/bin/bash

apt update

apt-get install -y tesseract-ocr

python3 cambiarRutaTesseract.py

python3 main.py
