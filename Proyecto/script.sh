#!/bin/bash
python3 hacerCambios.py
docker build -t app-flask .

docker-compose -f ./docker-compose.dev.yml up --build
python3 deshacerCambios.py
