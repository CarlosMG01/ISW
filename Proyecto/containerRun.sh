#!/bin/bash

# Lógica para determinar el valor de MYSQL_HOST
if [ -n "$1" ]; then
    MYSQL_HOST=$1
else
    MYSQL_HOST=127.0.0.1
fi

# Hacer cambios antes de levantar el contenedor
python3 hacerCambios.py

# Ejecutar docker-compose con o sin el parámetro MYSQL_HOST
if [ -n "$1" ]; then
    MYSQL_HOST=$1 docker-compose -f ./docker-compose.dev.yml up
else
    docker-compose -f ./docker-compose.dev.yml up
fi

# Deshacer cambios después de apagar el contenedor
python3 deshacerCambios.py
