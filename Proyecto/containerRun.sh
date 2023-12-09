#!/bin/bash
python3 hacerCambios.py

docker-compose -f ./docker-compose.dev.yml up 
python3 deshacerCambios.py
